import math

from game.matrix.Vector import Vector
from game.matrix.Matrix import Matrix

class Camera(object):
    # Generate the boundaries of the canvas. The canvas referenced here
    #   is the virtual camera's canvas, not the tkinter canvas.
    # The values are returned in order of NSEW (North, South, East, West)
    @staticmethod
    def generateCanvasCoordinates(clippingPlanes, fieldOfView, aspectRatio):
        (clipNearZ, clipFarZ) = clippingPlanes

        canvasRight  = float(math.tan(fieldOfView / 2) * clipNearZ)
        canvasLeft   = float(-canvasRight)
        canvasTop    = float(canvasRight / aspectRatio)
        canvasBottom = float(-canvasTop)

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

        projMatrix.values[0][0] = float(scaleFactor)
        projMatrix.values[1][1] = float(scaleFactor)
        projMatrix.values[2][2] = float(-clipFarZ / (clipFarZ - clipNearZ))
        projMatrix.values[3][2] = float(-clipFarZ*clipNearZ / (clipFarZ - clipNearZ))
        projMatrix.values[2][3] = float(-1)
        projMatrix.values[3][3] = float(0)

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
        cameraToWorldMatrix.values[0][0] = float(worldAxes[1].x)
        cameraToWorldMatrix.values[0][1] = float(worldAxes[1].y)
        cameraToWorldMatrix.values[0][2] = float(worldAxes[1].z)

        # y-axis
        cameraToWorldMatrix.values[1][0] = float(worldAxes[2].x)
        cameraToWorldMatrix.values[1][1] = float(worldAxes[2].y)
        cameraToWorldMatrix.values[1][2] = float(worldAxes[2].z)

        # z-azis
        cameraToWorldMatrix.values[2][0] = float(-worldAxes[3].x)
        cameraToWorldMatrix.values[2][1] = float(-worldAxes[3].y)
        cameraToWorldMatrix.values[2][2] = float(-worldAxes[3].z)

        # origin translation
        cameraToWorldMatrix.values[3][0] = float(origin.x)
        cameraToWorldMatrix.values[3][1] = float(origin.y)
        cameraToWorldMatrix.values[3][2] = float(origin.z)

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
        return self.worldToCameraMatrix.pointVectorMultiply(vectorW)

    def cameraToScreen(self, vectorC):
        # The screen should only show things in front of the camera (i.e.
        #   positive camera coords)
        if (vectorC.z > 0):
            return self.projMatrix.pointVectorMultiply(vectorC)
        else:
            return None

    def screenToRaster(self, vectorS, constrained):
        if (vectorS is None):
            return None

        x = vectorS.x
        y = vectorS.y

        # Screen coordinates must be within [-1,1] for raster projection
        # Here, instead of a strict [-1,1], there is a buffer added so that any
        #   vertices that are *just* off screen are drawn and the lines that
        #   end or begin on that point are also visualized.
        if (constrained and ((x < -1.1 or x > 1.1) or (y < -1.1 or y > 1.1))):
            return None
        else:
            # TODO: Decide in int() or roundHalfUp()
            # Normalize (x,y) to [0,1]
            normX = (x + 1) / 2
            normY = (y + 1) / 2

            # Scale the [0,1] to [0, dimension] where dimension is the image
            #   width or height depending on X or Y.
            rasterX = int(normX    *self.imageWidth )
            rasterY = int((1-normY)*self.imageHeight)

            return (rasterX, rasterY)

    # Take a world coordinate and tranform it to raster coordinates.
    def worldToRaster(self, vectorW, constrained):
        return self.screenToRaster(self.cameraToScreen(self.worldToCamera(vectorW)), constrained)

    # Given a list of world vectors, return a raster of the screen points.
    def generateRaster(self, listVectorW, constrained=False):
        raster = dict()

        for vectorW in listVectorW:
            rasterPos = self.worldToRaster(vectorW, constrained)

            if (rasterPos is not None):
                raster[rasterPos] = 255

        return raster
