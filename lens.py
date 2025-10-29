class Lens:
    @staticmethod
    def calculateImagePosition(focal_length: float, object_distance: float):
        if object_distance * focal_length == 0:
            return 1e9
        return (focal_length * object_distance) / (object_distance + focal_length)

    @staticmethod
    def calculateFocalLength(lens_refractive_index: float,
                             medium_refractive_index: float,
                             radius_of_curvature_1: float,
                             radius_of_curvature_2: float):
        n = lens_refractive_index / medium_refractive_index
        f_inv = (n - 1) * ((1 / radius_of_curvature_1) - (1 / radius_of_curvature_2))
        if f_inv == 0:
            return 1e9
        return 1 / f_inv
    
    @staticmethod
    def magnification(u: float, v: float):
        return v/u
