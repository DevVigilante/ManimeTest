from manim import *

class Intro(Scene):
    def construct(self):
        animatedBy = Text("Animated by Dev Kumar", font_size=18)
        animatedBy.to_corner(DR)
        animatedBy.set_opacity(0.5)
        self.add(animatedBy)
        text = Text("Innovative Creations of software technology", font_size=24)
        self.play(Write(text))
        self.wait(1)

        # Move it smoothly to bottom
        self.play(
            text.animate
            .scale(5)
            .fade(1),
            run_time=2
        )
        # self.play(text.animate.fade_to(color=None, alpha=0, family=None))
        self.wait(1)