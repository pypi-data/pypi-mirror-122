from PIL import Image, ImageDraw


# git tag 1.0.1 -m "PyPi tag"
# git push --tags origin master
# python setup.py sdist
# twine upload dist/*

def generate_image(orgs,options={}):

    sizeBoxX=options.get("sizeBoxX",200)
    sizeBoxY=options.get("sizeBoxY",120)
    paddingX=options.get("paddingX",10)
    paddingY=options.get("paddingY",20)
    arrowY=options.get("arrowY",10)
    defaultColor=options.get("defaultColor",'#384891')
    textColor=options.get("textColor",'black')

    orgs_ht={}
    maxboxes=max([len(org) for org in orgs])

    width=maxboxes*sizeBoxX
    height=sizeBoxY*len(orgs)

    img = Image.new("RGB",(width,height),'white')
    dr = ImageDraw.Draw(img)

    curY=0

    for line in orgs:
        print(line)
        shiftx=((maxboxes-len(line))*sizeBoxX)/(len(line)+1)
        startx=shiftx
        print(startx)
        for org in line:
            dr.rectangle([(startx+paddingX,curY+paddingY),(startx+sizeBoxX-paddingX,curY+sizeBoxY-paddingY-arrowY)]
                        ,outline=defaultColor,fill=org.get("fill",'white'),width=2)
            org["startArrowX"]=(startx+paddingX+startx+sizeBoxX-paddingX)/2
            org["startArrowY"]=curY+sizeBoxY-paddingY-arrowY
            org["endArrowY"]=curY+paddingY
            
            startx+=(sizeBoxX+shiftx)
            w, h = dr.textsize(org["name"])
            dr.text((org["startArrowX"]-(w/2),curY-(h/2)+paddingY+(sizeBoxY-2*paddingY-arrowY)/2), org["name"], org.get("color",textColor),align='center')
            
            orgs_ht[org["id"]]=org
        curY+=sizeBoxY    
    curY=0

    for line in orgs:
        startx=0
        for org in line:
            if "childs" in org and len(org["childs"])>0:
                dr.line([(org["startArrowX"],org["startArrowY"]),(org["startArrowX"],curY+sizeBoxY)], fill=defaultColor)
                for child in [orgs_ht[_] for _ in org["childs"] if _ in orgs_ht]:                
                    dr.line([(child["startArrowX"],curY+sizeBoxY),(org["startArrowX"],curY+sizeBoxY)], fill=defaultColor)
                    dr.line([(child["startArrowX"],child["endArrowY"]),(child["startArrowX"],curY+sizeBoxY)], fill=defaultColor)
                    dr.text((child["startArrowX"]+5,child["endArrowY"]-16), child.get('arrowtext','100%'),defaultColor)
        curY+=sizeBoxY     

    return img       


        