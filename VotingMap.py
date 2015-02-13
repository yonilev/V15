import shapefile
import bokeh.plotting as bok
import pandas as pd
from collections import OrderedDict
from bokeh.models import HoverTool

plot_width=400
plot_height=1000

df = pd.read_csv('data/data.csv')
israelRecord = shapefile.Reader('data/map/israel')
shape = israelRecord.shapeRecord(0).shape
longs = [p[0] for p in shape.points]
lats = [p[1] for p in shape.points]


oldMin = df.bzb_for_area.min()
oldMax = df.bzb_for_area.max()
newMin = 2
newMax = 12
oldRange = oldMax - oldMin  
newRange = newMax - newMin  

def transform(oldValue):
    return (((oldValue - oldMin) * newRange) / oldRange) + newMin

df.bzb_for_area_scaled = df.bzb_for_area.apply(lambda x: transform(x))
l = [('V', '#2166ac'),('VG', '#67a9cf'),('G', '#d1e5f0'),('I','#f7f7f7'),('P', '#fddbc7'),('MIX','#ef8a62'),('NO', '#b2182b')]
l.reverse()
colorMap = OrderedDict(l)
df.color = df.zone_classification.apply(lambda x: colorMap[x])





bok.output_file("map.html", title="V15")
TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave,hover"
dataSource = {}
dataSource['bzb']=df.bzb_for_area
dataSource['city']=df.city
dataSource['religion']=df.xeq_main_religion
source = bok.ColumnDataSource(data=dataSource)

p = bok.figure(title="Targeting Voters", tools=TOOLS,plot_width=plot_width, plot_height=plot_height)

p.patches([longs],[lats], fill_color="#d9d9d9", \
                line_color=None, \
                fill_alpha=0.8)


circles = p.circle(df.long,df.lat,radius=df.bzb_for_area_scaled,
       fill_color=df.color, fill_alpha=0.8,
       line_color=None, radius_units="screen",source=source)



# Configure hover:
hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([("City", "@city"),("Eligible Voters", "@bzb"),("Main Religion", "@religion")])

# Set legend
x, y = 34.4,32.7
for key,color in colorMap.iteritems():
    p.rect([x], [y], color=color, width=0.12, height=0.07)
    p.text([x+0.13], [y], text=key, angle=0, text_font_size="10pt", text_align="center", text_baseline="middle")
    y += 0.1



bok.show()

