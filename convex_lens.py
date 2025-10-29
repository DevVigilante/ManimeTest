from manim import *
from lens import *

class Intro(Scene):
    def construct(self):
        animatedBy = Text("Nature of convex lens changing to concave lens", font_size=24)
        animatedBy.to_corner(DR)
        animatedBy.set_opacity(0.5)
        self.add(animatedBy)
        text = Text("Innovative Creations of software technology", font_size=24)
        self.play(Write(text))
        self.wait(1)

        # Move it smoothly to bottom
        self.play(
            text.animate
            .scale(100)
            .fade(1),
            run_time=2
        )
        # self.play(text.animate.fade_to(color=None, alpha=0, family=>
        self.wait(1)

class ConvexLens(Scene):
    def construct(self):
        heading = Text(
            text="Nature of convex lens changing to concave lens",
            font_size=28
        )
        heading.to_corner(UL)
        self.play(Create(heading))
        self.wait(1)

        # Principal axis
        principal_axis = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        self.play(Create(principal_axis))
        self.wait(1)

        # Lens parameters
        objectDistance = -5
        radiusofSurface1 = 1.5
        radiusofSurface2 = 1.8
        medium_refractive_index = 1
        lens_refractive_index = 1.5

        ri_tracker = ValueTracker(medium_refractive_index)

        focalLengthTracker = ValueTracker(Lens.calculateFocalLength(
            lens_refractive_index,
            ri_tracker.get_value(),
            radiusofSurface1,
            -radiusofSurface2
        ))
        focalLengthTracker.add_updater(
            lambda m: m.set_value(
                Lens.calculateFocalLength(
                    lens_refractive_index,
                    ri_tracker.get_value(),
                    radiusofSurface1,
                    -radiusofSurface2
                )
            )
        )
        self.add(focalLengthTracker)

        # Lens shape
        lensSurface1 = Arc(
            radius=radiusofSurface1,
            start_angle=5 * PI / 6,
            angle=2 * PI / 6,
            color="#f3A8F2"
        )
        lensSurface1.move_arc_center_to(ORIGIN)

        lensSurface2 = Arc(
            radius=radiusofSurface2,
            start_angle=PI / 6,
            angle=-2 * PI / 6,
            color="#23A8F2"
        )
        lensSurface2.move_arc_center_to(ORIGIN)
        lensSurface1.next_to(lensSurface2, LEFT, buff=0)


        self.play(Create(lensSurface1), Create(lensSurface2))
        self.wait(1)

        # Centers and focus
        
        centre_of_curvature1 = Dot(
            lensSurface1.get_center() + [radiusofSurface1, 0, 0],
            color=YELLOW,
            radius=0.05
        )
        centre_of_curvature2 = Dot(
            lensSurface2.get_center() - [radiusofSurface2, 0, 0],
            color=YELLOW,
            radius=0.05
        )
        focus = Dot(
            color=PINK,
            radius=0.05
        )
        focus.add_updater(
            lambda foc:
                focus.next_to(lensSurface2, RIGHT, buff=focalLengthTracker.get_value())
        )
        focus.next_to(lensSurface2, RIGHT, buff=focalLengthTracker.get_value())

        self.play(GrowFromCenter(focus))
        self.wait(0.5)
        self.play(GrowFromCenter(centre_of_curvature1), GrowFromCenter(centre_of_curvature2))
        self.wait(0.5)

        # Tracker for object movement
        tracker = ValueTracker(objectDistance)

        # Function to create an arrow for object and image
        def create_arrow(position_x, height=1.0, color=GREEN):
            """Creates a vertical arrow with a head, base on the principal axis."""
            return Arrow(
                start=[position_x, 0, 0],
                end=[position_x, height, 0],
                buff=0,
                color=color,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25
            )

        # Create initial object and image arrows
        object_arrow = create_arrow(lensSurface1.get_center()[0] + tracker.get_value(), height=1.0, color=GREEN)
        image_arrow = create_arrow(
            lensSurface1.get_center()[0]
            + Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value()),
            height=Lens.magnification(
                tracker.get_value(),
                Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value())
            ),
            color=RED
        )

        self.play(GrowArrow(object_arrow))
        self.wait(0.5)
        self.play(GrowArrow(image_arrow))
        self.wait(0.5)

        # Updater for object arrow
        object_arrow.add_updater(
            lambda mob: mob.become(
                create_arrow(
                    lensSurface1.get_center()[0]
                    + tracker.get_value(),
                    height=1.0,
                    color=GREEN
                )
            )
        )

        # Updater for image arrow
        image_arrow.add_updater(
            lambda mob: mob.become(
                create_arrow(
                    lensSurface1.get_center()[0]
                    + Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value()),
                    height=Lens.magnification(
                        tracker.get_value(),
                        Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value())
                    ),  # scale height based on magnification
                    color=RED
                )
            )
        )
        
        value_text = always_redraw(
            lambda: VGroup(
                Text(
                    f"Focal length = {focalLengthTracker.get_value():.2f} m",
                     font_size=20,
                     color=PINK
                ),
                Text(
                  f"Medium RI = {ri_tracker.get_value():.2}",
                  font_size=20,
                  color="#009688"
                ),
                Text(
                  f"Lens RI = {lens_refractive_index:.2}",
                  font_size=20
                )
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(heading, DOWN, aligned_edge=LEFT)
        )
        self.play(Create(value_text))
        value_text2 = always_redraw(
            lambda: VGroup(
                Text(
                    f"Object distance = {tracker.get_value():.2f} m",
                    font_size=20,
                    color=GREEN),
                Text(
                    f"Image distance = {Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value()):.2f} m",
                    font_size=20,
                    color=RED
                ),
                Text(
                    f"Magnification = {Lens.magnification(tracker.get_value(), Lens.calculateImagePosition(focalLengthTracker.get_value(), tracker.get_value())):.2f}",
                    font_size=20,
                    color=YELLOW
                ),
                Text(
                    f"Radius of surface 1 = {radiusofSurface1}",
                    font_size=20,
                    color="#f3A8F2"
                ),
                Text(
                    f"Radius of surface 2 = {radiusofSurface2}",
                    font_size=20,
                    color="#23A8F2"
                )
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_corner(DL)
        )
        self.play(Create(value_text2))
        # Animate object movement
        self.play(tracker.animate.set_value(-0.1), run_time=20)
        self.wait(2)

        self.play(tracker.animate.set_value(-0.5), run_time=1)

        text = Text(
            """
            Now we will increase  refrative index of medium greater than lens,
            And the convex lens will behave as concave lens
            """, font_size=18)
        text.next_to(value_text2, RIGHT, buff=0.5)
        self.play(Write(text))
        self.wait(2)
        self.play(
                text.animate
                .fade(1),
            run_time=2
        )
        self.remove(text)
        self.wait(1)

        self.play(ri_tracker.animate.set_value(3), run_time=3)
        self.wait(1)
        self.play(tracker.animate.set_value(objectDistance), run_time=17)
        self.wait(5)
