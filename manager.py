#!/usr/bin/env python3

import multiprocessing
import nnt, worker

def StartWorker(level):
    p = multiprocessing.Process(target=worker.Start, args=(level,))
    p.start()

def StartWorkers():
    StartWorker(nnt.Logger.LEVEL.SPECIAL)
    StartWorker(nnt.Logger.LEVEL.CUSTOM)
    StartWorker(nnt.Logger.LEVEL.DEBUG)
    StartWorker(nnt.Logger.LEVEL.INFO)
    StartWorker(nnt.Logger.LEVEL.NOTICE)
    StartWorker(nnt.Logger.LEVEL.WARNING)
    StartWorker(nnt.Logger.LEVEL.ERROR)
    StartWorker(nnt.Logger.LEVEL.ALERT)
    StartWorker(nnt.Logger.LEVEL.CRITICAL)
    StartWorker(nnt.Logger.LEVEL.EMERGENCE)

if __name__ == "__main__":
    StartWorkers()