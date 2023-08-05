import numpy as np
from qec.protograph import protograph_to_qc_code,protograph_transpose,kron_mat_proto,kron_proto_mat
from qec.css import css_code

def I(n):
    '''
    Returns an identity matrix of size n
    '''
    return np.identity(n).astype(int)

class lifted_hgp(css_code):

    def __init__(self,lift_parameter,a,b=None):

        '''
        Generates the lifted hypergraph product of the protographs a and b
        '''
        self.a=a

        self.a_m,self.a_n=self.a.shape
        self.a_t=protograph_transpose(self.a)

        if b is None:
            self.b=np.copy(self.a)
        else:
            self.b=b
        
        self.b_t=protograph_transpose(self.b)
        self.b_m,self.b_n=self.b.shape

        self.hx1_proto=kron_proto_mat(self.a,I(self.b_n))
        self.hx2_proto=kron_mat_proto(I(self.a_m),self.b_t)
        self.hx_proto=np.hstack([self.hx1_proto,self.hx2_proto])

        self.hx1 = protograph_to_qc_code(lift_parameter,self.hx1_proto)
        self.hx2 = protograph_to_qc_code(lift_parameter,self.hx2_proto)
        self.hx=np.hstack([self.hx1,self.hx2]).astype(int)

        self.hz1_proto=kron_mat_proto(I(self.a_n),self.b)
        self.hz2_proto=kron_proto_mat(self.a_t,I(self.b_m))
        self.hz_proto=np.hstack([self.hz1_proto,self.hz2_proto])

        self.hz1=protograph_to_qc_code(lift_parameter,self.hz1_proto)
        self.hz2= protograph_to_qc_code(lift_parameter,self.hz2_proto)
        self.hz=np.hstack( [self.hz1, self.hz2] ).astype(int)

        super().__init__(self.hx,self.hz)

class lifted_bicycle(css_code):

    def __init__(self,lift_parameter,a,b=None):

        '''
        Generates the lifted hypergraph product of the protographs a and b
        '''

        a_m,a_n=a.shape
        a_T=protograph_transpose(a)

        if b is None:
            b=np.copy(a)
        
        b_T=protograph_transpose(b)
        b_m,b_n=b.shape

        self.hx1 = protograph_to_qc_code(lift_parameter, a)
        self.hx2 = protograph_to_qc_code(lift_parameter, b)
        self.hx=np.hstack([self.hx1,self.hx2]).astype(int)

        self.hz1=protograph_to_qc_code(lift_parameter, protograph_transpose(b))
        self.hz2= protograph_to_qc_code(lift_parameter, protograph_transpose(a))
        self.hz=np.hstack( [self.hz1, self.hz2] ).astype(int)

        super().__init__(self.hx,self.hz)

        self.lx1=self.lx[:,0:self.hx1.shape[1]]
        self.lx2=self.lx[:,self.hx1.shape[1]:]
        self.lz1=self.lz[:,0:self.hz1.shape[1]]
        self.lz2=self.lz[:,self.hz1.shape[1]:]