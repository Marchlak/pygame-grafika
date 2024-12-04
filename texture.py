import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/abc.jpg')
        self.textures[1] = self.get_texture(path='textures/grass.jpg')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox1/', ext='png')
        self.textures['skybox2'] = self.get_texture_cube(dir_path='textures/skybox2/', ext='png')
        self.textures['skybox3'] = self.get_texture_cube(dir_path='textures/skybox3/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()
        self.textures['staying_cat_texture'] = self.get_texture(
    path='objects/staying_cat/textures/Muchkin2_baseColor.png'  # Adjust the path and filename
)       
        self.textures['spinning_cat_texture'] = self.get_texture(
    path='objects/spinnig_cat/textures/dingus_baseColor.jpeg'  # Adjust the path and filename
)



    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert().convert_alpha()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=4,
                               data=pg.image.tostring(texture, 'RGBA', False))

        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
