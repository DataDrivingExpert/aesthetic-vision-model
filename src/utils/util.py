import os

img_path = "C:/Users/herre/Desktop/aesthetic research/suplementary_material/Data Sheet 2/Experiment 2 images/datasets/HLM/images"
label_path = "C:/Users/herre/Desktop/aesthetic research/suplementary_material/Data Sheet 2/Experiment 2 images/datasets/HLM/labels/train"

for i in range(63):
    filename = f"{i}_human_secuence"
    print(f"Deleting {filename}...")
    os.remove(os.path.join(label_path, filename + ".txt"))
    print("Deleted.")

    print(f"moving {filename}.png...")
    os.rename(os.path.join(img_path + '/train', filename + ".png"),
              os.path.join(img_path + '/redo', filename + ".png"))
    print("Moved.")

    print(f"{i=} done.")

    