#www.stuffaboutcode.com
#Raspberry Pi, Minecraft Bombs - Turn any block into a bomb!
 
#import the minecraft.py module from the minecraft directory
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
#import threading, so threads can be used
import threading
 
class LaserTunnel(threading.Thread):
 
    def __init__(self, pos, fuseInSecs, radius):
        # Setup object
        threading.Thread.__init__(self)
        self.pos = pos
        self.fuseInSecs = fuseInSecs
        self.radius = radius

 
    def run(self):
        #Open connect to minecraft
        mc = minecraft.Minecraft.create()
 
        #Get values
        pos = self.pos
        radius = self.radius
 
        #Explode the block!

        # get block type
        blockType = mc.getBlock(pos.x, pos.y, pos.z)

        # flash the block
        for fuse in range(0, self.fuseInSecs):
            mc.setBlock(pos.x, pos.y, pos.z, block.AIR)
            time.sleep(0.5)
            mc.setBlock(pos.x, pos.y, pos.z, blockType)
            time.sleep(0.5)

        # create sphere of air
        for z in range(-127, 127):
            for x in range (radius*-1, radius):
                for y in range (radius*-1, radius):
                    if x*x + y*y <= radius*radius:
                        mc.setBlock(pos.x + x, pos.y + y, pos.z + z, block.AIR)
 
if __name__ == "__main__":
 
    time.sleep(5)

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()
 
    #Post a message to the minecraft chat window
    mc.postToChat("Minecraft Laser, Hit (Right Click) a Fire! Credits: Evan, Kolya, Babusya & Grand Ivan")
 
    #loop until Ctrl C
    try: 
        while True:
            #Get the block hit events
            blockHits = mc.events.pollBlockHits()

            # if a block has been hit
            if blockHits:

                # for each block that has been hit
                for blockHit in blockHits:

                    #Create and run the exploding block class in its own thread
                    # pass the position of the block, fuse time in seconds and blast radius
                    # threads are used so multiple exploding blocks can be created

                    mc.postToChat("x=" + str(blockHit.pos.x) + "y=" + str(blockHit.pos.y) + "z=" + str(blockHit.pos.z))

                    laserBlock = LaserTunnel(blockHit.pos, 3, 4)
                    laserBlock.daemon
                    laserBlock.start()
                    time.sleep(0.1)
    except KeyboardInterrupt:

        print("stopped")
