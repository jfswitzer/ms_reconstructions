#!/usr/bin/env python3
"""
Image reconstruction in metashape
"""
import Metashape
import glob
import logging

def main():
    Metashape.app.gpu_mask = 2 ** (len(Metashape.app.enumGPUDevices())) - 1
    logging.basicConfig(filename='/extvol/metashape.log', level=logging.DEBUG)
    outfile = '/extvol/results.psx'
    doc = Metashape.Document()
    doc.read_only = False
    doc.save(outfile)    
    chunk = doc.addChunk() 
    photos = glob.glob('/extvol/images/*.png')
    logging.debug("START - Adding Files")    
    chunk.addPhotos(photos)
    logging.debug("DONE - Adding Files")
    logging.debug("START - Matching Files")        
    #chunk.matchPhotos(generic_preselection=True, reference_preselection=False)
    chunk.matchPhotos()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Matching Files")
    logging.debug("START - Aligning Files")            
    chunk.alignCameras()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Aligning Files")
    logging.debug("START - Optimizing Files")                
    chunk.optimizeCameras() #defaults are ok (match params in gui)
    doc.read_only = False    
    doc.save(outfile)    
    logging.debug("DONE - Optimizing Files")
    logging.debug("START - Resetting region")                    
    chunk.resetRegion()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Resetting region")                        
    logging.debug("START - Building depth maps")                    
    #chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.MildFiltering)
    chunk.buildDepthMaps()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building depth maps")
    logging.debug("START - Building dense cloud")
    chunk.resetRegion()    
    chunk.buildDenseCloud() #todo forum point?
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building dense cloud")
    logging.debug("START - Building model")                            
    #chunk.buildModel(surface_type=Metashape.Arbitrary, face_count=Metashape.HighFaceCount, interpolation=Metashape.EnabledInterpolation, vertex_colors=True)
    chunk.buildModel()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building model")
    logging.debug("START - Building UV")                                
    chunk.buildUV()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building UV")
    logging.debug("START - Building texture")                                    
    chunk.buildTexture()
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building texture")
    logging.debug("START - Building orthomosaic")

    chunk.buildOrthomosaic()
    #chunk.buildOrthomosaic(resolution_x=0.0701037, resolution_y=0.0701037)
    doc.read_only = False    
    doc.save(outfile)
    logging.debug("DONE - Building orthomosaic")                                        

if __name__=='__main__':
    main()
