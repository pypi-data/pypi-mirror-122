from ldpc.mod2 import nullspace
import numpy as np
from ldpc.codes import rep_code,ring_code
from ldpc.code_util import get_code_parameters
from qec.css import css_code
from qec.stab import stab_code
from qec.hgp import hgp
from qec.protograph import protograph_transpose,protograph_to_qc_code
from qec.lifted_hgp import lifted_hgp

def gf2_to_gf4(bin):
    n=int(len(bin)/2)
    gf4=np.zeros(n).astype(int)
    for i in range(n):
        if bin[i]==1 and bin[i+n]==0:
            gf4[i]=1
        elif bin[i]==0 and bin[i+n]==1:
            gf4[i]=3
        elif bin[i]==1 and bin[i+n]==1:
            gf4[i]=2

    return gf4

def hadamard_rotate(css_code,sector1_length):

    hx_css=css_code.hx
    hz_css=css_code.hz

    mx,n=hx_css.shape
    mz,nz=hz_css.shape

    assert n==nz

    hx=np.zeros((mx+mz,n)).astype(int)
    hz=np.zeros((mx+mz,n)).astype(int)

    hx[mz:,:sector1_length]=hx_css[:,:sector1_length]
    hx[:mz,sector1_length:]=hz_css[:,sector1_length:]

    hz[:mz,:sector1_length]=hz_css[:,:sector1_length]
    hz[mz:,sector1_length:]=hx_css[:,sector1_length:]

    return stab_code(hx,hz)

class xzzx_surface_code(stab_code):

    def __init__(self,nx,nz=None):

        if nz is None:
            nz=nx

        h1=rep_code(nx)
        h2=rep_code(nz)

        css_sc=hgp(h1,h2)
        xzzx_sc=hadamard_rotate(css_sc,css_sc.hx1.shape[1])

        self.__dict__=xzzx_sc.__dict__.copy()

        self.m1,self.n1=h1.shape
        self.m2,self.n2=h2.shape

        self.twist_boundaries()

    def twist_boundaries(self):

        for i in range(self.m1):

            self.hz[self.m2*self.n1+i*self.n2, i*self.n2+self.n2-1]=1
            self.hz[self.m2*self.n1+i*self.n2+(self.n2-1), (i+1)*self.n2]=1
            
        for i in range(self.m2):
            self.hx[i, self.n2*(self.n1-1) +i +1]=1
            self.hx[self.m2*(self.n1-1) +i, i]=1

        self.compute_logical_operators()
        self.h=np.hstack([self.hx,self.hz])
        self.l=np.hstack([self.lx,self.lz])

class xzzx_toric_code_old(stab_code):

    def __init__(self,nx,nz=None):

        if nz is None:
            nz=nx

        h1=ring_code(nx)
        h2=ring_code(nz)

        css_tc=hgp(h1,h2)
        xzzx_tc=hadamard_rotate(css_tc,css_tc.hx1.shape[1])

        self.__dict__=xzzx_tc.__dict__.copy()

        self.m1,self.n1=h1.shape
        self.m2,self.n2=h2.shape

        self.twist_boundaries()

    def twist_boundaries(self):

        hz1_n=self.n1*self.n2

        self.hz[:hz1_n,:hz1_n]=ring_code(hz1_n)
        self.hz[hz1_n:,hz1_n:]=ring_code(hz1_n).T

        self.compute_logical_operators()
        self.h=np.hstack([self.hx,self.hz])
        self.l=np.hstack([self.lx,self.lz])

    def to_css(self):

        hz1_n=self.n1*self.n2
        hz1=self.hz[:hz1_n,:hz1_n]
        hx2=self.hz[hz1_n:,hz1_n:]

        hx1=self.hx[hz1_n:,:hz1_n]
        hz2=self.hx[:hz1_n,hz1_n:]

        hx=np.hstack([hx1,hx2])
        hz=np.hstack([hz1,hz2])

        qcode_css=css_code(hx,hz)
        qcode_css.hx1=hx1
        qcode_css.hx2=hx2
        qcode_css.hz1=hz1
        qcode_css.hz2=hz2

        return qcode_css


class rotated_xzzx_code(stab_code):

    def __init__(self,nx,nz):

        n=nx*nz
        m=(nx-1)*(nz-1) + nz//2 +(nz-1)//2 +nx//2 +(nx-1)//2


        hx=np.zeros((m,n)).astype(int)
        hz=np.zeros((m,n)).astype(int)

        # print(hx)

        for j in range(nx-1):
            
            #main grid
            for k in range(nz-1):
                temp=j*(nz-1)
                hx[temp+k,j*(nz)+k]=1
                hx[temp+k,j*(nz)+k+nz+1]=1
                
                hz[temp+k,j*(nz)+k+1]=1
                hz[temp+k,j*(nz)+k+nz]=1

        temp=(nx-1)*(nz-1)
        count=0
        for j in range(0,nz-1,2):
            
            #the extra checks top
            hz[temp+count,j]=1
            hz[temp+count,(n-1)-(nz-1)+1+j]=1

            hx[temp+count,j+1]=1
            hx[temp+count,(n-1)-(nz-1)+j]=1

            count+=1
        
        temp=(nx-1)*(nz-1) + nz//2
        count=0
        for j in range(1,nz-1,2):
            #extra checks bottom

            hx[temp+count,j+1]=1
            hx[temp+count,(n-1)-(nz-1)+j]=1

            hz[temp+count,j]=1
            hz[temp+count,(n-1)-(nz-1)+1+j]=1

            count+=1
        
        temp=(nx-1)*(nz-1) + nz//2 +(nz-1)//2
        count=0
        for j in range(0,nx-1,2):

            #extra checks #right

            hz[temp+count,(j+1)*nz+nz-1]=1        
            hz[temp+count,j*nz]=1
            
            
            hx[temp+count,(j+1)*nz] =1
            hx[temp+count,j*nz+nz-1] =1

            count+=1


        temp=(nx-1)*(nz-1) + nz//2 +(nz-1)//2 +(nx)//2
        count=0
        for j in range(1,nx-1,2):

            #extra checks #left

            hz[temp+count,(j+1)*nz+nz-1]=1        
            hz[temp+count,j*nz]=1
            
            hx[temp+count,(j+1)*nz] =1
            hx[temp+count,j*nz+nz-1] =1

            count+=1


        super().__init__(hx,hz)
        self.nx=nx
        self.nz=nz

    def to_css(self):

        if not self.nx%2==0 and not self.nz%2:
            raise Exception(f"Attribute error: the XZZX code must have even lattice parameters to be converted to a CSS code. Not nx={self.nx} and nz={self.nz}.") 

        sector1_qubits=np.nonzero(nullspace(self.hx)[0])[0]
        sector2_qubits=np.nonzero(nullspace(self.hx)[1])[0]

        qubit_ordering=np.concatenate([sector1_qubits,sector2_qubits])

        print(qubit_ordering)

        self.hx=self.hx[:,qubit_ordering]
        self.hz=self.hz[:,qubit_ordering]

     
        temp1=np.copy(self.hx[:,self.N//2:])
        temp2=np.copy(self.hz[:,self.N//2:])

        self.hx[:,self.N//2:]=temp2
        self.hz[:,self.N//2:]=temp1

        delete_zero_rows = lambda mat: np.delete(mat,np.where(~mat.any(axis=1))[0], axis=0)
        self.hx=delete_zero_rows(self.hx)
        self.hz=delete_zero_rows(self.hz)

        print(self.hx)
        print(self.hz)

        # print(self.hx)
        # print(self.hz)

        return css_code(self.hx,self.hz)

class xzzx_toric_code(stab_code):
    def __init__(self,nx,nz):

        self.nx=nx
        self.nz=nz
        self.N=int(2*self.nx*self.nz)
        
        self.proto_1=np.array([[{0,1}]])
        self.proto_2=np.array([[{0,nz}]])

        self.css=lifted_hgp(self.N//2,self.proto_2,self.proto_1)

        lp=hadamard_rotate(self.css,self.N//2)

        # for key in lp.__dict__.keys():
        #     if key not in self.__dict__.keys():
        #         self.__dict__[key]=lp.__dict__[key]

        super().__init__(lp.hx,lp.hz)

    def to_css(self):
        return self.css


class xzzx_sc(stab_code):
    def __init__(self,nx,nz):        

        def Pfr(n,shift):
            base=np.hstack([np.identity(n-1),np.zeros((n-1,1))]).astype(int)
            perm=np.arange(n)
            perm=(perm-shift)%(n)
            return base[:,perm]

        N=nx*nz+(nx-1)*(nz-1)
        hz=Pfr(N,0)+Pfr(N,1)
        hx=Pfr(N,nz)+Pfr(N,(1-nz))
        super().__init__(hx,hz)


def main():

    print("Rotated XZZX codes")
    tsc=rotated_xzzx_code(4,3)
    tsc.test()
    # tsc=tsc.to_css()
    tsc.test()
    tsc.compute_code_distance()
    print(f"[[{tsc.N},{tsc.K},{tsc.D}]]")
    print(get_code_parameters(tsc.hx))
    print(get_code_parameters(tsc.hz))
    print()


    # print("Toric code lifted")
    # #xzzx toric from lifted product
    # tsc=xzzx_toric_code(2,2)
    # logicals=tsc.compute_code_distance(return_logicals=True)
    # tsc.test()
    # print(tsc.code_params)
    # print(logicals)
    # print()


    print("XZZX Surface code constructed")
    #xzzx toric from lifted product
    sc=xzzx_sc(3,2)
    logicals=sc.compute_code_distance(return_logicals=True)
    sc.test()
    print(sc.code_params)
    print(get_code_parameters(sc.hx))
    print(get_code_parameters(sc.hz))
    print(logicals)
    # print(sc.hz)
    # print(sc.hx)

    # assert np.array_equal(sc.hz,sc2.hz)

    # print(logicals)
    print()


if __name__ == "__main__":
    main()