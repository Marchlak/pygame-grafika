import pygame
from view.menu_view import MenuView
from di_container import DIContainer
from view.color_conversion_view import ColorConversionView
from model.color_model import ColorModel
from controller.color_conversion_controller import ColorConversionController
from components.resource_path import resource_path
from components.event_queue import EventQueue
from graphic_engine import GraphicsEngine

class MenuController:
    def __init__(self, screen):
        self.screen = screen
        self.view = MenuView(screen)
        self.active_controller = None
        self.is_opengl_mode = False
        self.di_container = DIContainer()
        self.di_container.register('ColorModel', ColorModel)
        self.di_container.register('ColorConversionView', lambda: ColorConversionView(self.screen))
        self.di_container.register('ColorConversionController', lambda: ColorConversionController(
            self.di_container.resolve('ColorModel'),
            self.di_container.resolve('ColorConversionView')))
        self.music_map = {
            "start_paint": resource_path("resources/paint_music.mp3"),
            "figure": resource_path("resources/cube_music.mp3"),
            "cone": resource_path("resources/cone_music.mp3"),
            "color": resource_path("resources/color_music.mp3"),
            "menu": resource_path("resources/menu_music.mp3"),
            "image": resource_path("resources/image.mp3"),
            "filter": resource_path("resources/filter.mp3"),
            "bin": resource_path("resources/bin.mp3"),
            "bezier": resource_path("resources/bezier.mp3"),
            "project": resource_path("resources/project.mp3"),
        }
        self.change_music("menu")
        self.event_queue = EventQueue()
        self.set_music_volume(1.0)

    def process_input(self):
        if self.active_controller:
            self.active_controller.process_input()
            if hasattr(self.active_controller, 'exit_request') and self.active_controller.exit_request:
                if self.is_opengl_mode:
                    self.active_controller.cleanup()
                    self.switch_to_pygame_mode()
                self.active_controller = None
                self.change_music("menu")
            return True

        # Handle menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                if self.view.is_hovering_nerd_image(event.pos):
                    self.view.show_tooltip = True
                else:
                    self.view.show_tooltip = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.view.get_button_action(event.pos)
                if action == "start_paint":
                    self.start_paint_controller()
                    self.change_music("start_paint")
                elif action == "figure":
                    self.start_figure_controller()
                    self.change_music("figure")
                elif action == "cone":
                    self.start_hsv_cone_controller()
                    self.change_music("cone")
                elif action == "color":
                    self.start_color_conversion_controller()
                    self.change_music("color")
                elif action == "filter":
                    self.start_filter_controller()
                    self.change_music("filter")
                elif action == "bfilter":
                    self.start_b_filter_controller()
                    self.change_music("filter")
                elif action == "image":
                    self.start_image_controller()
                    self.change_music("image")
                elif action == "histogram":
                    self.start_histogram_controller()
                    self.change_music("bin")
                elif action == "bbin":
                    self.start_basis_binarisation_controller()
                    self.change_music("bin")
                elif action == "bezier":
                    self.start_bezier_controller()
                    self.change_music("bezier")
                elif action == "analyze":
                    self.start_analyze_controller()
                    self.change_music("bezier")
                elif action == "project":
                    self.start_graphics_engine_controller()
                    self.change_music("projectt")
                elif action == "exit":
                    return False

        return True

    def update_view(self):
        if self.active_controller:
            self.active_controller.update_view()
        else:
            self.view.draw()

    def start_paint_controller(self):
        from controller.paint_controller import PaintController
        from model.paint_model import PaintModel
        from view.paint_view import PaintView

        model = PaintModel()
        view = PaintView(self.screen)
        self.active_controller = PaintController(model, view)

    def start_image_controller(self):
        from controller.image_controller import ImageController
        from model.ppm_image_model import PPMImageModel
        from view.image_view import ImageView

        model = PPMImageModel()
        view = ImageView(self.screen)
        self.active_controller = ImageController(model, view)

    def start_filter_controller(self):
        from controller.filter_controller import FilterController
        from view.filter_view import FilterView

        view = FilterView(self.screen)
        self.active_controller = FilterController(view)

    def start_b_filter_controller(self):
        from controller.b_filter_controller import BFilterController
        from view.b_filter_view import BFilterView

        view = BFilterView(self.screen)
        self.active_controller = BFilterController(view)

    def start_histogram_controller(self):
        from controller.histogram_controler import HistogramController
        from view.histogram_view import HistogramView
        from model.histogram_model import HistogramModel

        model = HistogramModel()
        view = HistogramView(self.screen)
        self.active_controller = HistogramController(view, model)

    def start_basis_binarisation_controller(self):
        from controller.basic_binarisation_controller import BasicBinarisationController
        from view.basic_binaristaion_view import BasicBinarisationView
        from model.basic_binarisation_model import BasicBinarisationModel
        model = BasicBinarisationModel()
        view = BasicBinarisationView(self.screen)
        self.active_controller = BasicBinarisationController(view, model)

    def start_figure_controller(self):
        self.switch_to_opengl_mode()
        from controller.figure_controller import FigureController
        from model.figure_model import FigureModel
        from view.figure_view import FigureView

        model = FigureModel()
        view = FigureView(self.screen)
        self.active_controller = FigureController(model, view)

    def start_hsv_cone_controller(self):
        self.switch_to_opengl_mode()
        from controller.hsv_controller import HSVConeController
        from model.figure_model import FigureModel
        from view.hsv_cone_view import HSVConeView

        model = FigureModel()
        view = HSVConeView(self.screen)
        self.active_controller = HSVConeController(model, view)

    def start_graphics_engine_controller(self):
        self.switch_to_opengl_mode()
        self.active_controller = GraphicsEngine(self.screen)
        self.is_opengl_mode = True

    def start_bezier_controller(self):
        from controller.bezier_controller import BezierController
        from model.bezier_model import BezierModel
        from view.bezier_view import BezierView

        model = BezierModel()
        view = BezierView(self.screen)
        self.active_controller = BezierController(model, view)

    def start_analyze_controller(self):
        from controller.analyze_controller import AnalyzeController
        from view.analyze_view import AnalyzeView
        from model.analyze_model import AnalyzeModel

        model = AnalyzeModel()
        view = AnalyzeView(self.screen)
        self.active_controller = AnalyzeController(view, model)

    def start_color_conversion_controller(self):
        self.active_controller = self.di_container.resolve('ColorConversionController')

    def switch_to_opengl_mode(self):
        # Ensure that pygame is not re-initialized
        pygame.display.quit()
        pygame.display.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
        self.screen = pygame.display.set_mode((1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Paint super aplikacja")
        try:
            icon_path = resource_path("resources/icon.png")
            icon_image = pygame.image.load(icon_path)
            pygame.display.set_icon(icon_image)
        except Exception as e:
            print("Brak ikonki")
        self.is_opengl_mode = True

    def switch_to_pygame_mode(self):
        pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.view = MenuView(self.screen)
        try:
            icon_path = resource_path("resources/icon.png")
            icon_image = pygame.image.load(icon_path)
            pygame.display.set_icon(icon_image)
        except Exception as e:
            print("Brak ikonki")
        self.is_opengl_mode = False

    def change_music(self, action):
        music_file = self.music_map.get(action)
        if music_file:
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)
                print(f"Muzyka zmieniona na: {music_file}")
            except Exception as e:
                print(f"Nie można załadować muzyki: {music_file}. Błąd: {e}")
        else:
            print(f"Brak przypisanej muzyki dla akcji: {action}")

    def set_music_volume(self, volume):
        if 0.0 <= volume <= 1.0:
            pygame.mixer.music.set_volume(volume)
            print(f"Głośność muzyki ustawiona na: {volume}")
        else:
            print("Głośność musi być w przedziale od 0.0 do 1.0")

