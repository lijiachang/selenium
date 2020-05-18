# coding:utf-8

txt = """
DatabaseSpaceFreeMB
DatabaseSpaceUsedMB
DatabaseSpaceUsedPCT
LogSpaceFreeMB
LogSpaceUsedMB
LogSpaceUsedPCT
SegSpace
SuspectIndex


"""
txt = txt.strip()

for x in txt.split("\n"):
    x = x.strip()
    print x[0].lower() + x[1:]
