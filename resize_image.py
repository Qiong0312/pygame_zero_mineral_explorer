from PIL import Image

# # List of frames to resize
# frame_names = ['move_1', 'move_2', 'move_3', 'move_4', 'move_5', 'move_6', 'move_7']

# for name in frame_names:
#     # Adjust file extension if your files are .jpg instead of .png
#     file_path = f'images/{name}.png' 

#     img = Image.open(file_path)
#     # Resize to 170x400
#     resized_img = img.resize((170, 400), Image.Resampling.LANCZOS)
#     resized_img.save(file_path)

# print("All character frames resized successfully!")

# List of frames to resize
frame_names = ['fluorite', 'apatite', 'talc', 'silver', 'amethyst', 'topaz', 'tungsten_carbide']
frame_names = ['opal']
frame_names = ['finger_nail_broken', 'nannys_teeth_broken', 'steel_axe_broken', 'bronze_bell_broken', 'toilet_fragment_broken']
frame_names = ['topaz']
frame_names = ['opal_powder', 'talc_powder', 'fluorite_powder', 'apatite_powder', 'silver_powder', 'amethyst_powder', 'topaz_powder', 'tungsten_carbide_powder']
frame_names = ['amethyst_powder', 'topaz_powder', 'tungsten_carbide_powder']
frame_names = ['the_intro_bg']
frame_names = ['star']
for name in frame_names:
    # Adjust file extension if your files are .jpg instead of .png
    file_path = f'images/{name}.png' 

    img = Image.open(file_path)
    # Resize to 60x60
    resized_img = img.resize((40, 40), Image.Resampling.LANCZOS)
    resized_img.save(file_path)

print("All character frames resized successfully! You can now use them in the game.")


