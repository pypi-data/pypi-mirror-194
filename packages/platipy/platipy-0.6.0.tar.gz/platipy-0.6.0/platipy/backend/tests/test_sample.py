import SimpleITK as sitk

from platipy.client import PlatiPyClient
from platipy.imaging import ImageVisualiser

api_key = "0f507d97-5e6e-42d8-92b8-35be937a735d"
pc = PlatiPyClient("localhost", 8808, api_key, "Bone Segmentation Sample")

ct_img = "/Users/60126181/Work/python/platipy/data/nifti/hn/TCGA_CV_5977/IMAGES/TCGA_CV_5977_1_CT_ONC_NECK_NECK_4.nii.gz"

ds = pc.add_dataset()
pc.add_data_object(ds, file_path=ct_img)

print(pc.get_dataset_ready(ds))

for x in pc.run_algorithm(ds):
    print(x)


print(pc.get_dataset(ds))

pc.download_output_objects(ds)

vis = ImageVisualiser(sitk.ReadImage(ct_img))
vis.add_contour(sitk.ReadImage("mask.nii.gz"), "bone")
fig = vis.show()
from matplotlib import pyplot as plt

plt.savefig("foo.png")
