#!/usr/bin/env python3
"""
Image reconstruction in metashape
"""
import Metashape
import glob

def main():
    #make sure that it knows to use gpus
    doc = Metashape.Document()
    chunk = doc.addChunk()
    photos = glob.glob('/extvol/images/*.png')
    chunk.addPhotos(photos)
    #todo not sure if reference preselection should be true or not
    chunk.matchPhotos(generic_preselection=True, reference_preselection=False)
    chunk.optimizeCameras() #defaults are ok (match params in gui)

    # align cameras
    chunk.alignCameras()

    # todo - optimize cameras

    #build depth map - todo not sure about depth value (should be 'medium')
    chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.MildFiltering)

    #build dense cloud
    chunk.buildDenseCloud()

    #build model/mesh
    chunk.buildModel(surface_type=Metashape.Arbitrary, face_count=Metashape.HighFaceCount, interpolation=Metashape.EnabledInterpolation, vertex_colors=True)

    # todo - what is this? do we need it?
    chunk.buildUV(mapping=Metashape.GenericMapping)

    #build texture
    chunk.buildTexture(blending=Metashape.MosaicBlending, texture_size=4096,fill_holes=True, ghosting_filter=True)
    #todo - confirm this step is needed for python 
    chunk.buildOrthomosaic(resolution_x=0.0701037, resolution_y=0.0701037)
    doc.save('result.psz')


if __name__=='__main__':
    main()
