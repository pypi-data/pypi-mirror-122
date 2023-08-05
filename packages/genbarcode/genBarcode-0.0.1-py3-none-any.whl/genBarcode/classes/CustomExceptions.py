# define Python user-defined exceptions
class NoImageViewerAvailable(Exception):
    """
        Define a custom exception for CLI/WSL
            IL.IPmageShow.show() during testing, tends to return True int(1) when passed
            to a viewer, or False int(0) when no viewer is available to display the image
    """

    def __init__(self):
        msg = "PIL was unable to find a useable image viewer"
        Exception.__init__(self, msg)
        self.message = msg
