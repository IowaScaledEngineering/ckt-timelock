#!/usr/bin/python

verString = "dxf2pcb version 1.5.5 - July 8, 2016"
# Written by Gabriel Denk of Aava Technology, LLC (Plano, TX)
# This software is released as-is.  No warrantee or guarantee is
#   expressed or implied as to the fitness, performance, or side-effects
#   of this code.
# This code is released under the Gnu Public License.  You are free to
#   use, modify, and distribute it, just keep the author's name and
#   company name attached it as in the comment block above.

#ToDo: Identify sections by GroupCode 0, not just by name.
#ToDo: Add switch to convert small circles to vias.
#ToDo: Read and use per-layer default line widths.
#ToDo: Add switch to create PCB primitives with lock flag set.

import sys
import os
import math
import traceback

DXFUnitsDict = {0:"unitless", 1:"inch", 2:"foot", 3:"mile", 4:"mm", 5:"cm", 6:"m",
                7:"km", 8:"uinch", 9:"mil", 10:"yard", 11:"angstrom", 12:"nm", 
                13:"um", 14:"dm", 15:"dam", 16:"hm", 17:"Gm", 18:"astronomical",
                19:"ly", 20:"parsec"}

class Line(object):
    'encapsulates a basic geometric line'
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.X1 = x1
        self.Y1 = y1
        self.X2 = x2
        self.Y2 = y2
        
    def FromPoints(self, pt1List, pt2List):
        self.X1 = pt1List[0]
        self.Y1 = pt1List[1]
        self.X2 = pt2List[0]
        self.Y2 = pt2List[1]
        
    @property
    def Midpoint(self):
        return [(self.X1+self.X2)/2, (self.Y1+self.Y2)/2]
    
    def __GetLength(self):
        return math.sqrt(abs(self.X1 - self.X2)**2 + abs(self.Y1 - self.Y2)**2)
    def __SetLength(self, newLen):
        lfact = newLen / self.Length
        [Xm, Ym] = self.Midpoint
        self.X1 = (self.X1 - Xm) * lfact + Xm
        self.Y1 = (self.Y1 - Ym) * lfact + Ym
        self.X2 = (self.X2 - Xm) * lfact + Xm
        self.Y2 = (self.Y2 - Ym) * lfact + Ym
    Length = property(__GetLength, __SetLength)

class Entity(object):
    'base class for specialized entity classes'

    Codes = dict.fromkeys(['8','10','20','30','370'], 0.0)
    DfltPenWidth = 7.0 #in mils
    UseLineWeightFromFile = False
    Clearance = 7.0 #in mils
    Mask = 3.5 #in mils
    #names of magic layers
    CopperLayer = 'copper'
    SilkLayer = 'silk'
    DrillLayer = 'pins'
    UnplatedDrillLayer = 'holes'
    LayerNamesAreCaseSensitive = True #if false, layer names above must be lowercase
    
    InUnitList = {"inch":1.0, "mm":1/25.4, "cm":1/2.54, "mil":0.001, "foot":12.0, "m":100/2.54, "um":1.0/25400}
    OutUnitList = {"mil":1000.0, "cmil":1e5, "mm":25.4}
    InputUnitConv = 1.0
    InputUnitLWConv = 1000.0  #input line weight conversion
    OutputUnits = "cmil"

    @staticmethod
    def SetGlobalInputUnits(unitString):
        if not unitString in Entity.InUnitList:
            raise Exception("Error: Invalid input units designator (must be among %s)." % Entity.GetInputUnitListString())
        Entity.InputUnitConv = Entity.InUnitList[unitString]

    @staticmethod
    def SetGlobalInputLWUnits(unitString):
        if not unitString in Entity.InUnitList:
            raise Exception("Error: Invalid input line weight units designator (must be among %s)." % Entity.GetInputUnitListString())
        Entity.InputUnitLWConv = Entity.InUnitList[unitString] * 1000.0
        
    @staticmethod
    def SetGlobalOutputUnits(unitString):
        if not unitString in Entity.OutUnitList:
            raise Exception("Error: Invalid output units designator (must be among %s)." % Entity.GetOutputUnitListString())
        Entity.OutputUnits = unitString        
        
    @staticmethod
    def GetInputUnitListString():
        outstr = ""
        for unitDes in Entity.InUnitList:
            outstr += unitDes + ", "
        return outstr[0:-2]

    @staticmethod
    def GetOutputUnitListString():
        outstr = ""
        for unitDes in Entity.OutUnitList:
            outstr += unitDes + ", "
        return outstr[0:-2]
    
    def __init__(self, codes):
        self.X1 = codes['10'] * Entity.InputUnitConv
        self.Y1 = codes['20'] * Entity.InputUnitConv
        if Entity.LayerNamesAreCaseSensitive:
            self.Layer = codes['8']
        else:
            self.Layer = codes['8'].lower()
        if codes['370'] <= 0.0 or not Entity.UseLineWeightFromFile:
            self.LineWeight = Entity.DfltPenWidth
        else:
            self.LineWeight = codes['370'] / 100.0
            self.LineWeight *= Entity.InputUnitLWConv #convert to mils
        
    def Translate(self, x, y):
        pass
    
    def FlipHorizontally(self, axisX):
        pass
    
    def FlipVertically(self, axisY):
        pass
    
    def Scale(self, factor):
        self.X1 *= factor
        self.Y1 *= factor
    
    def Print(self):
        print("--generic element--")

    def MaxX(self):
        return self.X1
        
    def MinX(self):
        return self.X1
        
    def MaxY(self):
        return self.Y1
        
    def MinY(self):
        return self.Y1
 
    def __Dist(self, x1, y1, x2, y2):
        return math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
    
    def Distance(self, otherEntity):
        return self.__Dist(self.X1, self.Y1, otherEntity.X1, otherEntity.Y1)
    
    def GetPCBFileSnippet(self):
        return "#nothing to see here"

    def GetElementSnippet(self):
        return "#nothing to see here"


class LineEntity(Entity):
    'encapsulates a line primitive'
    
    Codes = dict.fromkeys(['8','10','20','30','11','21','31','370'], 0.0)
    
    def __init__(self, codes):
        super(LineEntity, self).__init__(codes)
        self.X2 = codes['11'] * Entity.InputUnitConv
        self.Y2 = codes['21'] * Entity.InputUnitConv
        
    def Translate(self, x, y):
        self.X1 += x
        self.X2 += x
        self.Y1 += y
        self.Y2 += y

    def FlipHorizontally(self, axisX):
        self.X1 = 2 * axisX - self.X1
        self.X2 = 2 * axisX - self.X2
    
    def FlipVertically(self, axisY):
        self.Y1 = 2 * axisY - self.Y1
        self.Y2 = 2 * axisY - self.Y2
        
    def Scale(self, factor):
        super(LineEntity, self).Scale(factor)
        self.X2 *= factor
        self.Y2 *= factor

    def Print(self):
        lwStr = " LW = %0.2f" % self.LineWeight
        print("Line: (%f,%f) to (%f,%f) on layer %s%s" % (self.X1,self.Y1,self.X2,self.Y2,self.Layer,lwStr))
        
    def MaxX(self):
        return max(self.X1, self.X2)
        
    def MinX(self):
        return min(self.X1, self.X2)
        
    def MaxY(self):
        return max(self.Y1, self.Y2)
        
    def MinY(self):
        return min(self.Y1, self.Y2)

    def GetPCBFileSnippet(self):
        x1 = round(self.X1 * 1e5)
        x2 = round(self.X2 * 1e5)
        y1 = round(self.Y1 * 1e5)
        y2 = round(self.Y2 * 1e5)
        lw = round(self.LineWeight * 1e2)
        clr = round(LineEntity.Clearance * 1e2 * 2)
        return "Line[%d %d %d %d %d %d 0x00000020]\n" % (x1,y1,x2,y2,lw,clr)
    
    def GetElementSnippet(self):
        if self.Layer == Entity.SilkLayer:
            x1 = round(self.X1 * 1e5)
            x2 = round(self.X2 * 1e5)
            y1 = round(self.Y1 * 1e5)
            y2 = round(self.Y2 * 1e5)
            lw = round(self.LineWeight * 1e2)
            return "ElementLine[%d %d %d %d %d]\n" % (x1,y1,x2,y2,lw)
        else:
            raise Exception("Error:  Unsupported layer '%s' for line in element." % self.Layer)
        

class CircleEntity(Entity):
    'encapsulates a circle primitive'
    
    Codes = dict.fromkeys(['8','10','20','30','40','370'], 0.0)
    
    def __init__(self, codes):
        super(CircleEntity, self).__init__(codes)
        self.Radius = codes['40'] * Entity.InputUnitConv
        
    def Translate(self, x, y):
        self.X1 += x
        self.Y1 += y

    def FlipHorizontally(self, axisX):
        self.X1 = 2 * axisX - self.X1
    
    def FlipVertically(self, axisY):
        self.Y1 = 2 * axisY - self.Y1
        
    def Scale(self, factor):
        super(CircleEntity, self).Scale(factor)
        self.Radius *= factor

    def Print(self):
        lwStr = " LW = %0.2f" % self.LineWeight
        print("Circle: c(%f,%f) radius %f on layer %s%s" % (self.X1,self.Y1,self.Radius,self.Layer,lwStr))
        
    def MaxX(self):
        return self.X1 + self.Radius
        
    def MinX(self):
        return self.X1 - self.Radius
        
    def MaxY(self):
        return self.Y1 + self.Radius
        
    def MinY(self):
        return self.Y1 - self.Radius
    
    def GetPCBFileSnippet(self, convToHole=False):
        x = round(self.X1 * 1e5)
        y = round(self.Y1 * 1e5)
        width = height = round(self.Radius * 1e5)
        lw = round(self.LineWeight * 1e2)
        clr = round(CircleEntity.Clearance * 1e2 * 2)
        startAng = 0.0
        deltaAng = 360.0
        if convToHole:
            drill = width * 2
            snippet = 'Element["" "" "" "" %d %d 0 0 0 100 ""]\n' % (x,y)
            snippet += "(\n"
            snippet += '\tPin[0 0 %d %d %d %d "" "" "hole"]\n' % (drill,clr,drill,drill)
            snippet += ")\n"
            return snippet
        else:
            return "Arc[%d %d %d %d %d %d %0.1f %0.1f 0x00000020]\n" % (x,y,width,height,lw,clr,startAng,deltaAng)

    def GetElementSnippet(self, annulusEntity=None, pinNum=-1):
        x = round(self.X1 * 1e5)
        y = round(self.Y1 * 1e5)
        startAng = 0.0
        deltaAng = 360.0
        if self.Layer == Entity.SilkLayer:
            width = height = round(self.Radius * 1e5)
            lw = round(self.LineWeight * 1e2)
            return "ElementArc[%d %d %d %d %0.1f %0.1f %d]\n" % (x,y,width,height,startAng,deltaAng,lw)
        elif self.Layer == Entity.DrillLayer:
            if annulusEntity is None: raise Exception("Error:  Element pin cannot be generated without circle entity for annulus.")
            drill = round(self.Radius * 2 * 1e5)
            clr = round(CircleEntity.Clearance * 1e2 * 2)
            thk = round(annulusEntity.Radius * 2 * 1e5)
            msk = round(annulusEntity.Radius * 2 * 1e5 + self.Mask * 2 *1e2)
            if pinNum == -1: pn = ''
            else: pn = "%d" % pinNum
            if pinNum == 1: flags = "0x00000100"
            else: flags = "0x00000000"
            return 'Pin[%d %d %d %d %d %d "%s" "%s" %s]\n' % (x,y,thk,clr,msk,drill,pn,pn,flags)
        elif self.Layer == Entity.UnplatedDrillLayer:
            dia = round(self.Radius * 2 * 1e5)
            clr = round(CircleEntity.Clearance * 1e2 * 2)
            return 'Pin[%d %d %d %d %d %d "" "" 0x00000008]\n' % (x,y,dia,clr,dia,dia)
        else:
            raise Exception("Error:  Unsupported layer '%s' for circle in element." % self.Layer)

    @property
    def DiameterMils(self): return self.Radius * 2000

        
class ArcEntity(Entity):
    'encapsulates an arc primitive'
    
    Codes = dict.fromkeys(['8','10','20','30','40','50','51','370'], 0.0)
    
    def __init__(self, codes):
        super(ArcEntity, self).__init__(codes)
        self.Radius = codes['40'] * Entity.InputUnitConv
        self.StartAngle = codes['50']
        self.EndAngle = codes['51']
        
    def Translate(self, x, y):
        self.X1 += x
        self.Y1 += y

    def FlipHorizontally(self, axisX):
        self.X1 = 2 * axisX - self.X1
        self.StartAngle = (180 - self.StartAngle) % 360
        self.EndAngle = (180 - self.EndAngle) % 360
    
    def FlipVertically(self, axisY):
        self.Y1 = 2 * axisY - self.Y1
        self.StartAngle = 360 - self.StartAngle
        self.EndAngle = 360 - self.EndAngle
        
    def Scale(self, factor):
        super(ArcEntity, self).Scale(factor)
        self.Radius *= factor

    def Print(self):
        lwStr = " LW = %0.2f" % self.LineWeight
        print("Arc: c(%f,%f) radius %f from %fdeg to %fdeg on layer %s%s" % \
              (self.X1,self.Y1,self.Radius,self.StartAngle,self.EndAngle,self.Layer,lwStr))
        
    def __isAngleInArc(self, ang):
        a1 = self.StartAngle
        a2 = self.EndAngle
        if a2 < a1:
            if a1 > ang:
                a1 -= 360
            else:
                a2 += 360
        return a1 < ang and a2 > ang        
        
    def MaxX(self):
        if self.__isAngleInArc(0):
            cosine = 1
        else:
            cosine = math.cos(math.radians(self.StartAngle))
            cosine = max(cosine, math.cos(math.radians(self.EndAngle)))
        return self.X1 + self.Radius * cosine
        
    def MinX(self):
        if self.__isAngleInArc(180):
            cosine = -1
        else:
            cosine = math.cos(math.radians(self.StartAngle))
            cosine = min(cosine, math.cos(math.radians(self.EndAngle)))
        return self.X1 + self.Radius * cosine
        
    def MaxY(self):
        if self.__isAngleInArc(90):
            sine = 1
        else:
            sine = math.sin(math.radians(self.StartAngle))
            sine = max(sine, math.sin(math.radians(self.EndAngle)))
        return self.Y1 + self.Radius * sine
        
    def MinY(self):
        if self.__isAngleInArc(270):
            sine = -1
        else:
            sine = math.sin(math.radians(self.StartAngle))
            sine = min(sine, math.sin(math.radians(self.EndAngle)))
        return self.Y1 + self.Radius * sine

    def GetPCBFileSnippet(self):
        x = round(self.X1 * 1e5)
        y = round(self.Y1 * 1e5)
        width = height = round(self.Radius * 1e5)
        lw = round(self.LineWeight * 1e2)
        clr = round(ArcEntity.Clearance * 1e2 * 2)
        startAng = (180 - self.StartAngle) % 360
        deltaAng = (-(self.EndAngle-self.StartAngle)) % 360
        if deltaAng == 0 and abs(self.EndAngle-self.StartAngle) != 0: deltaAng = 360.0
        return "Arc[%d %d %d %d %d %d %0.1f %0.1f 0x00000020]\n" % (x,y,width,height,lw,clr,startAng,deltaAng)

    def GetElementSnippet(self, annulusEntity=None):
        x = round(self.X1 * 1e5)
        y = round(self.Y1 * 1e5)
        startAng = (180 - self.StartAngle) % 360
        deltaAng = (-(self.EndAngle-self.StartAngle)) % 360
        if self.Layer == Entity.SilkLayer:
            width = height = round(self.Radius * 1e5)
            lw = round(self.LineWeight * 1e2)
            return "ElementArc[%d %d %d %d %0.1f %0.1f %d]\n" % (x,y,width,height,startAng,deltaAng,lw)
        else:
            raise Exception("Error:  Unsupported layer '%s' for arc in element." % self.Layer)


class PolylineEntity(Entity):
    'encapsulates a polyline primitive'
    
    Codes = dict.fromkeys(['8','10','20','30','70','90','370'], 0.0)
    AutoCloseTolerance = 0.00001
    
    def __init__(self, codes, xlist, ylist):
        super(PolylineEntity, self).__init__(codes)
        if len(xlist) != len(ylist):
            raise Exception("Error:  Unpaired coordinates in polyline initialization.")
        if len(xlist) != int(codes['90']):
            raise Exception("Error:  Polyline vertex count mismatch.")
        if int(codes['70']) & 0x01 != 0: self.IsClosed = True
        elif (abs(xlist[0] - xlist[-1]) < PolylineEntity.AutoCloseTolerance
              and abs(ylist[0] - ylist[-1]) < PolylineEntity.AutoCloseTolerance): #auto-close
            self.IsClosed = True
            del xlist[-1] #delete last vertex because it is the same as the first
            del ylist[-1]
        else: self.IsClosed = False
        self.NumVertices = len(xlist)
        self.XList = xlist
        self.YList = ylist
        self.Scale(Entity.InputUnitConv)
        
    def Translate(self, x, y):
        for i in range(self.NumVertices):
            self.XList[i] += x
            self.YList[i] += y

    def FlipHorizontally(self, axisX):
        for i in range(self.NumVertices):
            self.XList[i] = 2 * axisX - self.XList[i]
    
    def FlipVertically(self, axisY):
        for i in range(self.NumVertices):
            self.YList[i] = 2 * axisY - self.YList[i]
        
    def Scale(self, factor):
        for i in range(self.NumVertices):
            self.XList[i] *= factor
            self.YList[i] *= factor

    def Print(self):
        lwStr = " LW = %0.2f" % self.LineWeight
        if self.IsClosed: shapeStr = "Polygon"
        else: shapeStr = "Polyline"
        print("%s:  with %d vertices on layer %s%s" % (shapeStr, self.NumVertices, self.Layer, lwStr))
        for i in range(self.NumVertices): print("   (%0.3f, %0.3f)" % (self.XList[i], self.YList[i]))
        
    def MaxX(self):
        return max(self.XList)
        
    def MinX(self):
        return min(self.XList)
        
    def MaxY(self):
        return max(self.YList)
        
    def MinY(self):
        return min(self.YList)

    def GetPCBFileSnippet(self):
        lw = round(self.LineWeight * 1e2)
        clr = round(LineEntity.Clearance * 1e2 * 2)
        if self.IsClosed:  #make closed polylines into polygons
            snippet = "Polygon(\"clearpoly\")\n(\n\t"
            for i in range(self.NumVertices):
                snippet += "[%d %d]" % (round(self.XList[i] * 1e5), round(self.YList[i] * 1e5))
                if i == self.NumVertices-1: snippet += "\n"
                elif i % 5 == 4: snippet += "\n\t"
                else: snippet += " "
            snippet += ")\n"
        else:  #make open polylines into multiple lines
            snippet = ""
            for i in range(self.NumVertices - 1):
                x1 = round(self.XList[i] * 1e5)
                x2 = round(self.XList[i+1] * 1e5)
                y1 = round(self.YList[i] * 1e5)
                y2 = round(self.YList[i+1] * 1e5)
                snippet += "Line[%d %d %d %d %d %d 0x00000020]\n" % (x1,y1,x2,y2,lw,clr)
        return snippet
        
    def GetElementSnippet(self, annulusEntity=None, pinNum=-1):
        if self.Layer == Entity.CopperLayer:
            if self.IsClosed:
                #ToDo: Check for non-rectangular pads.
                if len(self.XList) != 4:
                    raise Exception("Error:  Element pad designated with %d points (must be 4)." % len(self.XList))
                longSide = Line(self.XList[0], self.YList[0], self.XList[1], self.YList[1])
                shortSide = Line(self.XList[1], self.YList[1], self.XList[2], self.YList[2])
                if shortSide.Length > longSide.Length:
                    tmp = longSide
                    longSide = shortSide
                    shortSide = tmp
                    shortSide2 = Line(self.XList[2], self.YList[2], self.XList[3], self.YList[3])
                else:
                    shortSide2 = Line(self.XList[3], self.YList[3], self.XList[0], self.YList[0])
                thickness = shortSide.Length
                centerLine = Line()
                centerLine.FromPoints(shortSide.Midpoint, shortSide2.Midpoint)
                centerLine.Length = centerLine.Length - thickness
                thickness = round(thickness * 1e5)
                x1 = round(centerLine.X1 * 1e5)
                y1 = round(centerLine.Y1 * 1e5)
                x2 = round(centerLine.X2 * 1e5)
                y2 = round(centerLine.Y2 * 1e5)
                clr = round(PolylineEntity.Clearance * 1e2 * 2)
                msk = thickness + round(self.Mask * 2 * 1e2)
                if pinNum == -1: pn = ''
                else: pn = "%d" % pinNum
                return 'Pad[%d %d %d %d %d %d %d "%s" "%s" 0x00000100]\n' % (x1,y1,x2,y2,thickness,clr,msk,pn,pn)
            else:
                raise Exception("Error:  Unsupported layer '%s' for open polygons in element." % self.Layer)
        elif self.Layer == Entity.SilkLayer:            
            snippet = ""
            lw = round(self.LineWeight * 1e2)
            for i in range(self.NumVertices - 1):
                x1 = round(self.XList[i] * 1e5)
                x2 = round(self.XList[i+1] * 1e5)
                y1 = round(self.YList[i] * 1e5)
                y2 = round(self.YList[i+1] * 1e5)
                snippet += "ElementLine[%d %d %d %d %d]\n" % (x1,y1,x2,y2,lw)
            if self.IsClosed:
                x1 = round(self.XList[-1] * 1e5)
                x2 = round(self.XList[0] * 1e5)
                y1 = round(self.YList[-1] * 1e5)
                y2 = round(self.YList[0] * 1e5)
                snippet += "ElementLine[%d %d %d %d %d]\n" % (x1,y1,x2,y2,lw)                
            return snippet
        else:
            raise Exception("Error:  Unsupported layer '%s' for polyline in element." % self.Layer)
        


def GetDxfGroup(dxfFile, lineNum):
    groupCode = dxfFile.next().strip()
    value = dxfFile.next().strip()
    if not groupCode.isdigit():
        raise Exception("DXF file formatting error: Expecting group code, found %s (line %d)." % (groupCode, lineNum-1))
    groupCode = int(groupCode)
    if groupCode < -5 or groupCode > 1071:
        raise Exception("DXF file formatting error: Group code %d is out of range (line %d)." % (groupCode, lineNum-1))
    return groupCode, value
 
def ParsePolylineSection(dxfFile):
    xlist = []
    ylist = []
    codes = PolylineEntity.Codes
    while True:
        groupCode = dxfFile.next().strip()
        if groupCode == '0':
            break
        datValue = dxfFile.next().strip()
        if groupCode in codes:
            try:
                if int(groupCode) >= 10:
                    datValue = float(datValue)
            except:
                raise Exception("Error:  Improper formatting in DXF file.")
            if groupCode == '10': xlist.append(datValue)
            elif groupCode == '20': ylist.append(datValue)
            else: codes[groupCode] = datValue
    codes['10'] = xlist[0]
    codes['20'] = ylist[0]
    retObj = PolylineEntity(codes, xlist, ylist)
    return retObj
        
def ParseEntitySection(dxfFile, entityType):
    if entityType == "LINE":
        codes = LineEntity.Codes
    elif entityType == "CIRCLE":
        codes = CircleEntity.Codes
    elif entityType == "ARC":
        codes = ArcEntity.Codes
    elif entityType == "LWPOLYLINE":
        return ParsePolylineSection(dxfFile)
    while True:
        groupCode = dxfFile.next().strip()
        if groupCode == '0':
            break
        datValue = dxfFile.next().strip()
        if groupCode in codes:
            try:
                if int(groupCode) >= 10:
                    datValue = float(datValue)
            except:
                raise Exception("Error:  Improper formatting in DXF file.")
            codes[groupCode] = datValue

    if entityType == "LINE":
        retObj = LineEntity(codes)
    elif entityType == "CIRCLE":
        retObj = CircleEntity(codes)
    elif entityType == "ARC":
        retObj = ArcEntity(codes)
    return retObj

def IndentString(instr):
    retVal = "\t" + instr.replace("\n", "\n\t")
    if retVal.endswith('\t'): retVal = retVal[0:-1]
    return retVal

def DisplayHelpText():
    #                                                                                     |80                 |100
    print("Usage: dxf2pdf.py -switch1 [argument1] -switch2 [argument2]")
    print("Available switches:            (Notes)/[Examples]:")
    print("  -out outputFilePathAndName   [-out ~/pcb_data/brd_outline.pcb]")
    print("  -in inputFilePathAndName     [-in ~/drawings/outline.dxf]")
    print("  -xl excludedLayer1,exLayer2  [-xl 0,DEFAULT1,ALL_AXIS]")
    print("  -inf                         (displays file information only)")
    print("  -lst                         (lists all drawing entities processed)")
    print("  -sol outputLayer             (sets output layer number in pcb file) [-sol 3]")
    print("  -lw lineWeight               (sets default line weight in mils) [-lw 6.5]")
    print("  -olw                         (override line weights in DXF file)")
    print("  -clr clearanceInPolygons     (sets copper clearance in mils) [-clr 7.5]")
    print("  -msk solderMaskClr           (sets default mask clearance in mils) [-msk 3.5]")
    print("  -scl scalingFactor           (scales all drawing by factor) [-scl 2.3]")
    print("  -dmo                         (do not move to origin)")
    print("  -cth holeSize                (convert circles smaller than x mils to holes) [-cth 250]")
    print("  -el                          (generate output as element, -dmo is implied -")
    print("                                this feature requires specific layer names:")
    print("                                %s, %s, %s, %s)" % (Entity.CopperLayer, Entity.DrillLayer, Entity.UnplatedDrillLayer, Entity.SilkLayer))
    print("  -an                          (auto-number pins/pads based on order of DXF file)")
    print("  -iun inputUnits              (set input units--%s) [-iun %s]" 
          % (Entity.GetInputUnitListString(), Entity.InUnitList.keys()[1]))
    print("  -ilu inputLineweightUnits    (set units for input line weights) [-ilu %s]" % Entity.InUnitList.keys()[0])
    #print("  -oun outputUnits             (set output units--%s) [-oun %s]"
    #      % (Entity.GetOutputUnitListString(), Entity.OutUnitList.keys()[1]))
    print("  -v                           (verbose/debug mode)")
    print("\n" + verString)

#==============================================================================

try:
    #parse command line args
    i = 1
    
    inFileName = ''
    outFileName = ''
    layerExcludeList = []
    infoOnly = False
    doListing = False
    outLayerNumber = 1
    solSwitchUsed = False
    lineWidth = 7.0
    useLineWeightFromFile = True
    clearance = 7.0
    maskClearance = 3.5
    scalingFactor = 1
    doMoveToOrigin = True
    circleToHoleThresh = 0.0 #diameter
    elementMode = False
    autoNumber = False
    inputUnits = ""
    inputLWUnits = ""
    outputUnits = ""
    verboseMode = False

    print("")
    
    if len(sys.argv) <= 1:
        DisplayHelpText()
        raise Exception("\nDone!\n")
    
    while i < len(sys.argv):
        if sys.argv[i] == '-in':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -in switch.")
            inFileName = sys.argv[i+1]
            if inFileName[0] == '-' and len(inFileName) in [2,3,4]:
                raise Exception("Error: Missing argument for -in switch.")
            print("Input File: " + inFileName)
            i += 2
        elif sys.argv[i] == '-out':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -out switch.")
            outFileName = sys.argv[i+1]
            if outFileName[0] == '-' and len(outFileName) in [2,3,4]:
                raise Exception("Error: Missing argument for -out switch.")
            print("Output File: " + outFileName)
            i += 2
        elif sys.argv[i] == '-xl': #layer exclusion
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -xl switch.")
            layerExcludeList = sys.argv[i+1].split(',')
            print("Layers Excluded:")
            for layerName in layerExcludeList:
                print("  " + layerName)
            i += 2
            pass
        elif sys.argv[i] == '-inf': #just get information about the file
            infoOnly = True
            print("Displaying information only, no output file created.")
            i += 1
        elif sys.argv[i] == '-lst':
            doListing = True
            print("Including list of drawing entities.")
            i += 1
        elif sys.argv[i] == '-sol':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -sol switch.")
            outLayerNumber = sys.argv[i+1]
            if outLayerNumber[0] == '-' and len(outLayerNumber) in [2,3,4]:
                raise Exception("Error: Missing argument for -sol switch.")
            if not outLayerNumber.isdigit():
                raise Exception("Error: Output layer number must be an integer.")
            outLayerNumber = int(outLayerNumber)
            print("Creating output on PCB layer %d." % outLayerNumber)
            solSwitchUsed = True
            i += 2
        elif sys.argv[i] == '-lw':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -lw switch.")
            try:
                lineWidth = float(sys.argv[i+1])
            except:
                raise Exception("Error: Invalid number format for -lw switch argument \"%s\"." % sys.argv[i+1])
            print("Line weight default set to %0.2f mils." % lineWidth)
            i += 2
        elif sys.argv[i] == '-olw': #override line weights in file with default
            useLineWeightFromFile = False
            print("Overriding line weights from DXF file.")
            i += 1
        elif sys.argv[i] == '-clr':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -clr switch.")
            try:
                clearance = float(sys.argv[i+1])
            except:
                raise Exception("Error: Invalid number format for -clr switch argument \"%s\"." % sys.argv[i+1])
            print("Line/arc clearance set to %0.2f mils." % clearance)
            i += 2
        elif sys.argv[i] == '-msk':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -msk switch.")
            try:
                maskClearance = float(sys.argv[i+1])
            except:
                raise Exception("Error: Invalid number format for -msk switch argument \"%s\"." % sys.argv[i+1])
            print("Mask clearance default set to %0.2f mils." % maskClearance)
            i += 2
        elif sys.argv[i] == '-scl':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -scl switch.")
            try:
                scalingFactor = float(sys.argv[i+1])
            except:
                raise Exception("Error: Invalid number format for -scl switch argument \"%s\"." % sys.argv[i+1])
            print("Scaling drawing by a factor of %0.3f." % scalingFactor)
            i += 2
        elif sys.argv[i] == '-dmo':
            doMoveToOrigin = False
            print("Not moving drawing to origin.")
            i += 1
        elif sys.argv[i] == '-cth':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -cth switch.")
            try:
                circleToHoleThresh = float(sys.argv[i+1])
            except:
                raise Exception("Error: Invalid number format for -cth switch argument \"%s\"." % sys.argv[i+1])
            print("Circles smaller than %0.1f mils in diameter will be converted to holes." % circleToHoleThresh)
            i += 2
        elif sys.argv[i] == '-el':
            elementMode = True
            doMoveToOrigin = False
            print("Generating element output, omitting move to origin.")
            i += 1
        elif sys.argv[i] == '-an': #enable auto-numbering
            autoNumber = True
            print("Automatically numbering pins/pads.")
            i += 1
        elif sys.argv[i] == '-iun':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -iun switch.")
            inputUnits = sys.argv[i+1]
            Entity.SetGlobalInputUnits(inputUnits)
            print("Input units set to %s." % inputUnits)
            i += 2
        elif sys.argv[i] == '-ilu':
            if len(sys.argv) < i+2:
                raise Exception("Error: Missing argument for -ilu switch.")
            inputLWUnits = sys.argv[i+1]
            i += 2
#         elif sys.argv[i] == '-oun':
#             if len(sys.argv) < i+2:
#                 raise Exception("Error: Missing argument for -oun switch.")
#             outputUnits = sys.argv[i+1]
#             Entity.SetGlobalOutputUnits(outputUnits)
#             print("Output units set to %s." % outputUnits)
#             i += 2
        elif sys.argv[i] == '-v':
            verboseMode = True
            print("Verbose messages enabled.")
            i += 1
        elif sys.argv[i] == '-?' or sys.argv[i] == '--help':
            DisplayHelpText()
            raise Exception("\nDone!\n")
        else:
            if sys.argv[i][0] == '-':
                raise Exception("Error: Unknown switch \"%s\" encountered." % (sys.argv[i]))
            else:
                raise Exception("Error: Unknown argument \"%s\" encountered." % (sys.argv[i]))
            
    if elementMode and solSwitchUsed:
        print("Warning: Cannot set layer of an element, -sol switch ignored.")
        
    Entity.DfltPenWidth = lineWidth
    Entity.Clearance = clearance
    Entity.Mask = maskClearance
    Entity.UseLineWeightFromFile = useLineWeightFromFile
    
    if inputLWUnits:
        if not useLineWeightFromFile:
            print("Warning: Line weights overridden by -olw switch, ignoring -ilu switch.")
        else:
            Entity.SetGlobalInputLWUnits(inputLWUnits)
            print("Input line weight units set to %s." % inputLWUnits)
    
    #if input units are specified but line weight units are not, use input units for line weights also
    if inputUnits and not inputLWUnits:
        inputLWUnits = inputUnits
        Entity.SetGlobalInputLWUnits(inputLWUnits)
    
    if inputUnits:
        if verboseMode: print("Input unit scaling factor: %0.8f" % Entity.InputUnitConv)
        
    #open input file
    if len(inFileName) == 0 or not os.path.exists(inFileName):
        raise Exception("Error: File \"%s\" not found." % inFileName)
    dxfFile = open(inFileName, 'r')
    
    #open output file
    if not infoOnly:
        if len(outFileName) == 0:
            raise Exception("Error: No output file specified.")
        pcbFile = open(outFileName, 'w')

    #extract info from file header, stop at entities section
    unitString = ""
    lineNum = 2
    grpCode, value = GetDxfGroup(dxfFile, lineNum)
    while True:
        if grpCode == 9 and value == '$INSUNITS':
            grpCode, value = GetDxfGroup(dxfFile, lineNum)
            lineNum += 2
            if grpCode == 70:
                if not value.isdigit(): print("Warning: Invalid drawing units designation in DXF file, ignoring.")
                else:
                    unitString = DXFUnitsDict[int(value)]
                    if not unitString in Entity.InUnitList:
                        print("Warning: Unknown drawing units designation '%s' in DXF file, ignoring." % unitString)
                        unitString = ""
        elif grpCode == 2 and value == 'ENTITIES': break
        grpCode, value = GetDxfGroup(dxfFile, lineNum)
        lineNum += 2
            
    if unitString and not inputUnits:
        Entity.SetGlobalInputUnits(unitString)
        if verboseMode: print("Input units set from DXF file: %s" % unitString)
        if not inputLWUnits: Entity.SetGlobalInputLWUnits(unitString)
            
    if verboseMode: print("Entities section found at line %d." % lineNum)
    
    #extract entities (of supported types) from input file
    entityList = []
    layerList = []
    knownEntities = ['LINE', 'CIRCLE', 'ARC', 'LWPOLYLINE']
    for txtLine in dxfFile:
        txtLine = txtLine.strip()
        if txtLine in knownEntities:
            entity = ParseEntitySection(dxfFile, txtLine)
            if entity.Layer not in layerList:
                layerList.append(entity.Layer)
            if entity.Layer not in layerExcludeList:
                entityList.append(entity)
        
    #scale drawing if requested
    if scalingFactor != 1:
        for entity in entityList:
            entity.Scale(scalingFactor)
        
    #find extents of drawing
    minX = minY = 1e9
    maxX = maxY = -1e9
    for entity in entityList:
        minX = min(minX, entity.MinX())
        maxX = max(maxX, entity.MaxX())
        minY = min(minY, entity.MinY())
        maxY = max(maxY, entity.MaxY())
    width = maxX - minX
    height = maxY - minY
    
    if verboseMode: print("Processing %d primitives." % len(entityList))
    
    #display info if requested
    if infoOnly:
        print("Layers:")
        for layerName in layerList:
            print("   "+layerName)
        print("Extents:")
        print("   Min X = %f" % minX)
        print("   Min Y = %f" % minY)
        print("   Max X = %f" % maxX)
        print("   Max Y = %f" % maxY)
        print("   Width = %f" % width)
        print("   Height = %f" % height)

    #not just displaying info, proceed with processing
    else:
        #translate to PCB coordinate system and move drawing to origin
        if doMoveToOrigin:
            for entity in entityList:
                entity.Translate(-minX, -minY)
                entity.FlipVertically(height/2)
        else:
            for entity in entityList:
                entity.FlipVertically(0.0)
        if elementMode:
            annulusList = []
            for entity in entityList:
                if type(entity) == CircleEntity and entity.Layer == Entity.CopperLayer:
                    annulusList.append(entity)
            #generate element file
            pinNum = 1
            pcbFile.write('Element[0x00000000 "" "" "" 1000 1000 0 0 0 100 0x00000000]\n')
            pcbFile.write("(\n")
            for entity in entityList:
                if type(entity) == CircleEntity:
                    if entity.Layer == Entity.CopperLayer: continue
                    elif entity.Layer == Entity.DrillLayer: #pin with annulus
                        annulusFound = False
                        for annulus in annulusList:
                            if entity.Distance(annulus) < 0.0001:
                                if autoNumber:
                                    pcbFile.write(IndentString(entity.GetElementSnippet(annulus, pinNum)))
                                    pinNum += 1
                                else:
                                    pcbFile.write(IndentString(entity.GetElementSnippet(annulus)))
                                annulusList.remove(annulus)
                                annulusFound = True
                                break
                        if not annulusFound:
                            raise Exception("Error:  Could not find annulus circle for pin at (%0.3f, %0.3f)." % (entity.X1, entity.Y1))
                    else:
                        pcbFile.write(IndentString(entity.GetElementSnippet()))
                else:
                    if type(entity) == PolylineEntity and entity.Layer == Entity.CopperLayer:
                        pcbFile.write(IndentString(entity.GetElementSnippet(None, pinNum)))
                        pinNum += 1
                    else:
                        pcbFile.write(IndentString(entity.GetElementSnippet()))
            pcbFile.write(")\n")
            if verboseMode:
                print("%d pins automatically numbered." % (pinNum-1))
        else:
            #generate PCB file
            pcbFile.write("PCB[\"\" %d %d]\n\n" % (round(width*1e5), round(height*1e5)))
            pcbFile.write("Grid[100.0 0 0 0]\n")
            pcbFile.write("Layer(%d \"Layer%d\")\n" % (outLayerNumber, outLayerNumber))
            pcbFile.write("(\n")
            for entity in entityList:
                if type(entity) != CircleEntity or entity.DiameterMils >= circleToHoleThresh:
                    pcbFile.write(IndentString(entity.GetPCBFileSnippet()))
            pcbFile.write(")\n")
            for entity in entityList:
                if type(entity) == CircleEntity and entity.DiameterMils < circleToHoleThresh:
                    pcbFile.write(IndentString(entity.GetPCBFileSnippet(True)))
        pcbFile.close()
    
    #list all elements if requested
    if doListing:
        print("")
        print("Entity Listing:")
        for entity in entityList:
            entity.Print()
    
    print("\nDone!\n")
                
except Exception, arg:
    print(arg)
    if verboseMode: traceback.print_tb(sys.exc_info()[-1], 50)
    try:
        pcbFile.close()
    except:
        pass
    try:
        dxfFile.close()
    except:
        pass
