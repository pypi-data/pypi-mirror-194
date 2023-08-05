from py_arkworks_bls12381 import G1Point, G2Point, Scalar

# Copies the interface for py-ecc


# This is the identity point or point at infinity
Z1 = G1Point.identity()
# Generator point for G1
G1 = G1Point()
# Generator point for G2
G2 = G2Point()

def KeyValidate(b) -> bool:
    # We can just use py_ecc for this
    pass

def add(lhs : G1Point, rhs : G1Point) -> G1Point:
    return lhs + rhs

def neg(point : G1Point) -> G1Point:
    return -point

def multiply(point : G1Point, integer : int) -> G1Point:
    # This is a python integer. `Scalar` can only 
    # be initialized with u128 with the constructor. So lets convert the
    # integer to bytes and then initialise the `Scalar` using a byte array
    int_as_bytes = integer.to_bytes(32, 'little')
    scalar = Scalar.from_le_bytes(int_as_bytes)
    return point * scalar

def bytes48_to_G1(bytes48) -> G1Point:
    # This will do subgroup checks
    return G1Point.from_bytes(bytes48)

def G1_to_bytes48(point : G1Point) -> bytes:
    # This will do subgroup checks
    return point.to_bytes()

def bytes96_to_G2(bytes96) -> G1Point:
    # This will do subgroup checks
    return G2Point.from_bytes(bytes96)

def G2_to_bytes96(point : G2Point) -> bytes:
    # This will do subgroup checks
    return point.to_bytes()