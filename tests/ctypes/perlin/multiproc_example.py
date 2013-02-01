# import multiprocessing

# class MyFancyClass(object):
    
#     def __init__(self, name):
#         self.name = name
    
#     def do_something(self):
#         proc_name = multiprocessing.current_process().name
#         print 'Doing something fancy in %s for %s!' % (proc_name, self.name)


# def worker(q):
#     obj = q.get()
#     obj.do_something()


# if __name__ == '__main__':
#     queue = multiprocessing.Queue()

#     p = multiprocessing.Process(target=worker, args=(queue,))
#     p.start()
    
#     queue.put(MyFancyClass('Fancy Dan'))
    
#     # Wait for the worker to finish
#     queue.close()
#     queue.join_thread()
#     p.join()

import multiprocessing
import time

from noise import _simplex, _perlin

class ProcessingRange(object):
    def __init__(self, size, pos, pmax, face):
        self._size = size
        self._pos  = pos
        self._max  = pmax
        self._face = face

        self._xstart = 0
        self._xend   = 0
        self._ystart = 0
        self._yend   = 0
        self._zstart = 0
        self._zend   = 0

        self._setup()

    @property
    def x_start(self):
        return self._xstart

    @property
    def x_end(self):
        return self._xend

    @property
    def y_start(self):
        return self._ystart

    @property
    def y_end(self):
        return self._yend

    @property
    def z_start(self):
        return self._zstart

    @property
    def z_end(self):
        return self._zend

    @property
    def face(self):
        return self._face

    @property
    def pos(self):
        return self._pos

    def _setup(self):
        p_range = self._size / self._max
        start = self._pos * p_range
        end = start + p_range

        # TOP
        if self._face == 0:
            self._xstart = start
            self._xend   = end
            self._ystart = self._size
            self._yend   = -1
            self._zstart = 0
            self._zend   = self._size

        # BACK
        if self._face == 1:
            self._xstart = start
            self._xend   = end
            self._ystart = 0
            self._yend   = self._size
            self._zstart = -self._size
            self._zend   = -1

        # RIGHT
        if self._face == 2:
            self._xstart = self._size
            self._xend   = -1
            self._ystart = 0
            self._yend   = self._size
            self._zstart = start
            self._zend   = end

        # BOTTOM
        if self._face == 3:
            self._xstart = start
            self._xend   = end
            self._ystart = -self._size
            self._yend   = -1
            self._zstart = 0
            self._zend   = self._size

        # FRONT
        if self._face == 4:
            self._xstart = start
            self._xend   = end
            self._ystart = 0
            self._yend   = self._size
            self._zstart = self._size
            self._zend   = -1

        # LEFT
        if self._face == 5:
            self._xstart = -self._size
            self._xend   = -1
            self._ystart = 0
            self._yend   = self._size
            self._zstart = start
            self._zend   = end

class Task(object):
    def __init__(self):
        pass

    def __call__(self):
        pass

        
    def __str__(self):
        pass

class NoiseTask(Task):

    """Perlin Noise Process"""
    #def __init__(self, size, pos, x_start, x_end):
    def __init__(self, pr):
        Task.__init__(self)
        # self._size = size
        # self._x_start = x_start
        # self._x_end = x_end
        # self._pos = pos

        self._pr = pr

        self._perlin_data = []
  
    def __str__(self):
        #return "Task face: %d x_start: %d x_end: %d" % (self._pr.face)
        return "Task face: %d" % (self._pr.face)

    def get_position(self):
        return self._pos

    def get_noise(self):
        return self._perlin_data

    # def __call__(self):
    #     self._perlin_data = []
    #     z = 0.5
    #     octaves = 6
    #     scale = 2 * octaves
    #     ls3 = 10 * octaves
    #     ls2 = 15 * octaves
    #     ls = 20 * octaves

    #     for x in range(self._x_start, self._x_end):
    #         for y in xrange(self._size):
    #             value = _perlin.noise3(float(x) / ls, float(y) / ls, z, octaves, 0.5)#, base=0)

    #             if value > 0.8 or value < 0:
    #                 value = -1
    #             else:
    #                 value += _perlin.noise3(float(x) / scale, float(y) / scale, z, octaves, 0.5)#, base=0)
    #                 value += _perlin.noise3(float(x) / ls2, float(y) / ls2, z, octaves, 0.5)#, base=0)
    #                 value += _perlin.noise3(float(x) / ls3, float(y) / ls3, z, octaves, 0.5)#, base=0)
    #                 value = value * 127.0 + 128.0
    #             self._perlin_data += [value, value, value, 1.0]

    #     return [self._pos, self._perlin_data]

    def __call__(self):

        octaves = 6.0
        ioct = int(octaves)
        scale = 2 * octaves
        ls3 = 10 * octaves
        ls2 = 15 * octaves
        ls = 20 * octaves

        # If the FRONT or BACK
        if self._pr.face == 4 or self._pr.face == 1:
            z = self._pr.z_start
            x_start = self._pr.x_start
            x_end = self._pr.x_end
            y_end = self._pr.y_end

            for x in range(x_start, x_end):
              for y in xrange(y_end):

                value = _perlin.noise3(x / ls, y / ls, z / ls, ioct, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls2, ioct, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                self._perlin_data += [value, value, value, 1.0] 

        # if the TOP or BOTTOM
        elif self._pr.face == 0 or self._pr.face == 3:
            y = self._pr.y_start

            x_start = self._pr.x_start
            x_end = self._pr.x_end
            z_end = self._pr.z_end

            for x in range(x_start, x_end):
              for z in xrange(z_end):

                value = _perlin.noise3(x / ls, y / ls, z / ls, ioct, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls3, ioct, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                self._perlin_data += [value, value, value, 1.0]


        # if the RIGHT or LEFT
        elif self._pr.face == 2 or self._pr.face == 5:
            x = self._pr.x_start

            y_end  = self._pr.y_end
            z_start = self._pr.z_start
            z_end = self._pr.z_end

            for z in range(z_start, z_end):
              for y in xrange(y_end):

                value = _perlin.noise3(x / ls, y / ls, z / ls, ioct, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, ioct, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls3, ioct, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                self._perlin_data += [value, value, value, 1.0]
                
        return [self._pr.face, self._pr.pos, self._perlin_data]

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means we should exit
                print '%s: Exiting' % proc_name
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.result_queue.put(answer)
        return

if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    # num_jobs = 10
    # for i in xrange(num_jobs):
    #     tasks.put(Task(i, i))

    size = 2048
    num_jobs = 8

    trange = size / num_jobs
    for i in range(0, num_jobs):
        tasks.put(NoiseTask(size, i, i*trange, (i*trange)+trange))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)
    
    # Start printing results
    while num_jobs:
        result = results.get()
        #print 'Result:', result
        num_jobs -= 1
    print "Finished"