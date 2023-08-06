from koala.classes import *

# File
filename = 'example2'

# Layers
gold_layer = ly.layer(0, 0)
polymer_layer = ly.layer(1, 0)
border_layer = ly.layer(2, 0)
mask_layer = ly.layer(3, 0)

# Parameters mask (all dimensions in um)
maskY = 210000
maskX = 297000

# Parameters substrate
substrateX = 75000
substrateY = 25000
marginPrint = 750

marginY = 3500
marginX = 3500

# Text
marginTextX = 1500
marginTextY = 2500

# Parameter channel
channelWidth = 2000
channelLength = 500
electrodeHeight = 1000

# Parameters tracks
trackWidth = 300
padSize = 2500
trackLength = substrateY/2 - electrodeHeight - channelLength/2 - marginY
marginContactElectrode = 50

# Electrodes
contact_cell = Cell('CONTACT')
electrode = Rectangle('electrode', channelWidth, electrodeHeight, dx=0, dy=trackLength + electrodeHeight/2)
pad = Rectangle('pad', padSize, padSize)
points_track = [db.Point(0, padSize/2), db.Point(0, trackLength)]
track = Path(points_track, trackWidth)

contact_cell.draw_polygon(electrode, gold_layer)
contact_cell.draw_polygon(pad, gold_layer)
contact_cell.draw_polygon(pad, polymer_layer)
contact_cell.draw_path(track, gold_layer)

# Device
device_cell = Cell('DEVICE')
channel = Rectangle('channel', channelWidth, channelLength + 2*marginContactElectrode, dx=0, dy=substrateY/2)

device_cell.insert_cell(contact_cell, 0, marginY)
device_cell.insert_cell(contact_cell, 0, substrateY - marginY, 180, 1)
device_cell.draw_polygon(channel, polymer_layer)

# Substrate
substrate_cell = Cell('SUBSTRATE')
substrate = Rectangle('substrate', substrateX, substrateY)
substrate_cell.insert_cell(device_cell, substrateX/4, 0)
substrate_cell.insert_cell(device_cell, 3 * substrateX/4, 0)

# Text
text_cell = Cell("TEXT")
text = Text("W/L: " + str(channelWidth) + '/' + str(channelLength) + '', 1000)
text_cell.draw_text(text, gold_layer)
substrate_cell.insert_cell(text_cell, substrateX/2, substrateY/2)


# Alignment marks
alignment_cell = Cell('ALIGNMENT', ALIGN_SQUARE_PATH)
[substrate_cell.insert_cell(alignment_cell, substrateX/2 + i*5000, substrateY/2 + j*5000) for i in [-1, 1] for j in [-1, 1]]

# substrate_cell.flatten()
substrate_cell.export_design_gds(filename)
substrate_cell.export_layer_gds(filename)

