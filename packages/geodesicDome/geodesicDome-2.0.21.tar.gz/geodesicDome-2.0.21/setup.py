from setuptools import find_packages, setup






setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='2.0.21',
    long_description="""Module geodesic_dome
====================

Classes
-------

`GeodesicDome(freq=0)`
:   Class wrapper to create and interact with a Geodesic Dome
    
    Creates a given geodesic dome with a given frequency.
    
    Args:
        freq (int, optional): The frequency of the geodesic dome. Defaults to 0.

    ### Methods

    `find_neighbours(self, index: numpy.int64, depth=1) ‑> numpy.ndarray`
    :   Finds the neighbours of a given vertex on the geodesic dome to a certain depth (defaults to 1 if not provided)
        
        Args:
            index (np.int64): The index of the vertex to search from
            depth (int, optional): The depth of neighbours to return. Defaults to 1.
        
        Returns:
            np.ndarray: An array containing the indices of all the vertex's neighbours

    `get_triangles(self) ‑> numpy.ndarray`
    :   Getter function for triangles
        
        Returns:
            np.ndarray: the triangles of the geodesic dome

    `get_vertices(self) ‑> numpy.ndarray`
    :   Getter function for vertices
        
        Returns:
            np.ndarray: the vertices of the geodesic dome

    `tessellate(self, freq=1) ‑> None`
    :   Tessellates the geodesic dome a given number of times (tessellates once if no arguments provided)
        
        Args:
            freq (int, optional): The number of times to tessellate. Defaults to 1.""",
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
    
   
)