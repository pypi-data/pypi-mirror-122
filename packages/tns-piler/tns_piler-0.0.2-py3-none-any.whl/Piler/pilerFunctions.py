import gffutils

def getTranscriptExonBoundaries(transcriptID, db): # generator
    for exon in db.children(db[transcriptID], featuretype="exon"):
        yield (exon.chrom, exon.start, exon.stop, exon.strand)

def getPiles(handledBAM, boundaryTuple):
    out=[]
    for pileupcolumn in handledBAM.pileup(boundaryTuple[0], boundaryTuple[1]-1, boundaryTuple[2]-1):
        if pileupcolumn.pos >= boundaryTuple[1]-1 and pileupcolumn.pos <= boundaryTuple[2]-1:
            out.append(pileupcolumn.n)
    if (boundaryTuple[2] - boundaryTuple[1] + 1) != len(out):
        raise Exception("Something Uh Oh with get Piles")

    return out
        

def getCumulativePileups(piles):
    total = sum(piles)
    out=[]
    running_total=0
    
    for pile in piles:
        running_total+=pile
        out.append(running_total/total)
        
    return out
