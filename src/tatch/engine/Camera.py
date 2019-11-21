import math

from matrix.Vector import Vector
from matrix.Matrix import Matrix

class Camera(object):
    # Generate the boundaries of the canvas. The canvas referenced here
    #   is the virtual camera's canvas, not the tkinter canvas.
    # The values are returned in order of NSEW (North, South, East, West)
    @staticmethod
    def generateCanvasCoordinates(clippingPlanes, fieldOfView, aspectRatio):
        (clipNearZ, clipFarZ) = clippingPlanes

        canvasRight  = math.tan(fieldOfView / 2) * clipNearZ
        canvasLeft   = -canvasRight
        canvasTop    = canvasRight / aspectRatio
        canvasBottom = -canvasTop

        return (canvasTop, canvasBottom, canvasRight, canvasLeft)

    # Create the projection matrix according to 3D perspective projection.
    # The projection matrix M converts from camera space coordinates into
    #   projections on the camera canvas. These formulas work best when
    #   the camera is at our near the near clipping plane.
    # To generate the matrix, the clipping plane locations and the field
    #   of view are the sole variables needed.
    @staticmethod
    def generateProjectionMatrix(clippingPlanes, fieldOfView):
        (clipNearZ, clipFarZ) = clippingPlanes
        scaleFactor = 1 / ( math.tan( (fieldOfView / 2) * (math.pi / 180) ) )

        # Create the 4x4 matrix shell to populate with data, then populate
        projMatrix = Matrix(4,4)

        projMatrix.values[0][0] = scaleFactor
        projMatrix.values[1][1] = scaleFactor
        projMatrix.values[2][2] = -clipFarZ / (clipFarZ - clipNearZ)
        projMatrix.values[3][2] = -clipFarZ*clipNearZ / (clipFarZ - clipNearZ)
        projMatrix.values[2][3] = -1
        projMatrix.values[3][3] = 0

        return projMatrix

    # The CameraToWorld matrix defines that camera's transormations with respect
    #   to the world coordinate system. This, then, is the camera's position
    #   and orientation in the world, and this has the effect of storing the
    #   information needed to convert a coordinate from world to camera space.
    #   Multiplying a vector in world space by this matrix gives a vector in
    #   camera space.
    # It is important to note that this is the standard camera orientation. That
    #   is, the camera is oriented along the negative z-axis.
    @staticmethod
    def generateCameraToWorldMatrix(worldAxes):
        cameraToWorldMatrix = Matrix.generateIdentity(4,4)

        origin = worldAxes[0]

        # x-axis
        cameraToWorldMatrix.values[0][0] = worldAxes[1].x
        cameraToWorldMatrix.values[0][1] = worldAxes[1].y
        cameraToWorldMatrix.values[0][2] = worldAxes[1].z

        # y-axis
        cameraToWorldMatrix.values[1][0] = worldAxes[2].x
        cameraToWorldMatrix.values[1][1] = worldAxes[2].y
        cameraToWorldMatrix.values[1][2] = worldAxes[2].z

        # z-azis
        cameraToWorldMatrix.values[2][0] = -worldAxes[3].x
        cameraToWorldMatrix.values[2][1] = -worldAxes[3].y
        cameraToWorldMatrix.values[2][2] = -worldAxes[3].z

        # origin translation
        cameraToWorldMatrix.values[3][0] = origin.x
        cameraToWorldMatrix.values[3][1] = origin.y
        cameraToWorldMatrix.values[3][2] = origin.z

        return cameraToWorldMatrix

    # Initialize the Camera object and generate all transformation matrices
    def __init__(self, fieldOfView, clippingPlanes, imageDim, worldAxes):
        # Store the instance variables and calculate aspect ratio
        self.fieldOfView = fieldOfView
        self.clippingPlanes = clippingPlanes
        self.worldAxes = worldAxes
        (self.imageWidth, self.imageHeight) = imageDim
        self.aspectRatio = self.imageWidth / self.imageHeight


        # Calculate all perspective information

        (self.cTop, self.cBottom, self.cRight, self.cLeft) =\
            Camera.generateCanvasCoordinates(clippingPlanes, fieldOfView,\
                self.aspectRatio)

        self.projMatrix = Camera.generateProjectionMatrix(clippingPlanes,\
            fieldOfView)
        self.cameraToWorldMatrix =\
            self.generateCameraToWorldMatrix(self.worldAxes)
        self.worldToCameraMatrix = Matrix.inverse(self.cameraToWorldMatrix)

    def worldToCamera(self, vectorW):
        output = self.worldToCameraMatrix.pointVectorMultiply(vectorW)
        return output

    def cameraToScreen(self, vectorC):
        # The screen should only show things in front of the camera (i.e.
        #   positive camera coords)
        if (vectorC.z > 0):
            output = self.projMatrix.pointVectorMultiply(vectorC)
            return output
        else:
            return None

    def screenToRaster(self, vectorS, constrained):
        if (vectorS is None):
            return None

        # Get the (x,y) point from the screen vector since the (z) is unneeded
        (x,y) = (vectorS.x, vectorS.y)

        # Screen coordinates must be within [-1,1] for raster projection
        if (constrained and ((x < -1 or x > 1) or (y < -1 or y > 1))):
            return None
        else:
            # TODO: Decide in int() or roundHalfUp()
            # Normalize (x,y) to [0,1]
            normX = (x + 1) / 2
            normY = (y + 1) / 2

            rasterX = int(min(self.imageWidth -1,normX    *self.imageWidth ))
            rasterY = int(min(self.imageHeight-1,(1-normY)*self.imageHeight))

            return(rasterX, rasterY)

    # Take a world coordinate and tranform it to raster coordinates.
    def worldToRaster(self, vectorW, constrained):
        return self.screenToRaster(self.cameraToScreen(self.worldToCamera(vectorW)), constrained)

    # Generate a raster given a list of world vectors.
    def generateRaster(self, listVectorW, constrained=True):
        raster = dict()

        for vectorW in listVectorW:
            rasterPos = self.worldToRaster(vectorW, constrained)

            if (rasterPos is not None):
                raster[rasterPos] = 255

        return raster