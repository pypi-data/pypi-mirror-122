import numpy as np
from qec.hgp import hgp_single,hgp
# from .hgp3d import hgp3d
from ldpc.codes import rep_code,ring_code,hamming_code
from .css import css_code
from ldpc.code_util import compute_code_distance
# from .lifted_hgp import lifted_hgp, lifted_bicycle


'''
[[4,2,2]] detection code
'''

class det422(css_code):
    def __init__(self):
        hx=np.array([[1,1,1,1]])
        hz=np.array([[1,1,1,1]])
        super().__init__(hx,hz)
        self.name="det422"

'''
The Steane Code
'''
class steane_code(css_code):
    def __init__(self,g=3):
        if g<3: raise Exception("g must be equal or larger than 3")

        super().__init__()
        self.hx=hamming_code(g)
        self.hz=hamming_code(g)
        self.K=self.compute_dimension()
        self.D=3
        self.lx,self.lz=self.compute_logicals()
        self.name=f"steane_{g}"

'''
2D topological codes
'''

class surface_code(hgp):
    def __init__(self,n1,n2=None):
        if n2 is None: n2=n1
        h1=rep_code(n1)
        h2=rep_code(n2)
        super().__init__(h1,h2,compute_distance=True)
        self.compute_ldpc_params()
        self.name=f"surface_{self.D}"


class toric_code(hgp):
    def __init__(self,n1,n2=None):
        if n2 is None: n2=n1
        h1=ring_code(n1)
        h2=ring_code(n2)
        super().__init__(h1,h2,compute_distance=True)
        self.compute_ldpc_params()
        self.name=f"toric_{self.D}"


# '''
# 3D Topological codes
# '''

# class toric_code_3d(hgp3d):
#     def __init__(self,distance):
#         h=ring_code(distance)
#         super().__init__(h)
#         if self.K==np.nan: self.compute_dimension()
#         self.compute_ldpc_params()
#         self.name=f"toric3d_{distance}"

# class surface_code_3d(hgp3d):
#     def __init__(self,distance):
#         h=rep_code(distance)
#         super().__init__(h,h,h.T)
#         if self.K==np.nan: self.compute_dimension()
#         self.compute_ldpc_params()
#         self.name=f"surface3d_{distance}"


# '''
# Lifted Product Codes
# '''

# def qldpc(code_name):

#     print(code_name)

#     if code_name is "p19b1":

#         lift_parameter=63

#         proto_a = np.array([
#                 [{27}, {}, {}, {}, {}, {0}, {54}],
#                 [{54}, {27}, {}, {}, {}, {}, {0}],
#                 [{0}, {54}, {27}, {}, {}, {}, {}],
#                 [{}, {0}, {54}, {27}, {}, {}, {}],
#                 [{}, {}, {0}, {54}, {27}, {}, {}],
#                 [{}, {}, {}, {0}, {54}, {27}, {}],
#                 [{}, {}, {}, {}, {0}, {54}, {27}]
#             ])

#         proto_b = np.array([
#                 [{0, 62, 57}]
#             ])

#         return lifted_hgp(lift_parameter,proto_a,proto_b)

#     if code_name is "p19b2":

#         lift_parameter=63

#         proto_a = np.array([
#                 [{27}, {}, {}, {0}, {18}, {27}, {0}],
#                 [{0}, {27}, {}, {}, {0}, {18}, {27}],
#                 [{27}, {0}, {27}, {}, {}, {0}, {18}],
#                 [{18}, {27}, {0}, {27}, {}, {}, {0}],
#                 [{0}, {18}, {27}, {0}, {27}, {}, {}],
#                 [{}, {0}, {18}, {27}, {0}, {27}, {}],
#                 [{}, {}, {0}, {18}, {27}, {0}, {27}]
#             ])

#         proto_b = np.array([
#                 [{0, 62, 57}]
#             ])

#         return lifted_hgp(lift_parameter,proto_a,proto_b)

#     if code_name is "p19b3":

#         lift_parameter=127

#         proto_a = np.array([
#                 [{0}, {}, {51}, {52}, {}],
#                 [{}, {0}, {}, {111}, {20}],
#                 [{0}, {}, {98}, {}, {122}],
#                 [{0}, {80}, {}, {119}, {}],
#                 [{}, {0}, {5}, {}, {106}]
#             ])

#         proto_b = np.array([
#                 [{0, 126, 120}]
#             ])

#         return lifted_hgp(lift_parameter,proto_a,proto_b)

#     if code_name is "tanner":

#         lift_parameter=31

#         proto_a = np.array([
#                 [{1},{2},{4},{8},{16}],
#                 [{5},{10},{20},{9},{18}],
#                 [{25},{19},{7},{14},{28}]
#             ])

#         return lifted_hgp(31,proto_a)

#     if code_name is "p19a1":

#         '''
#         Bicycle code A1 from p19
#         '''

#         a=np.array([[{0,15,20,28,66}]])
#         b=np.array([[{0,58,59,100,121}]])

#         return lifted_bicycle(127,a,b)


#     if code_name is "p19a2":

#         '''
#         Bicycle code A1 from p19
#         '''

#         a=np.array([[{0,1,14,16,22}]])
#         b=np.array([[{0,3,13,20,42}]])

#         return lifted_bicycle(63,a,b)


    
 

