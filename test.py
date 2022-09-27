import torch
import segmentation_models_pytorch as smp
import torchvision.transforms as transforms
from torchvision import models

import pickle

from PIL import Image
import matplotlib.pyplot as plt

def pallette_plot(output_predictions):
    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")

    # plot the semantic segmentation predictions of 21 classes in each color
    r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(input_image.size)
    r.putpalette(colors)
    # plt.imshow(r)
    # plt.show()
    return r


if __name__ == '__main__':
    # model = smp.Unet(
    #     encoder_name="resnet34",        # choose encoder, e.g. mobilenet_v2 or efficientnet-b7
    #     encoder_weights="imagenet",     # use `imagenet` pre-trained weights for encoder initialization
    #     in_channels=1,                  # model input channels (1 for gray-scale images, 3 for RGB, etc.)
    #     classes=3,                      # model output channels (number of classes in your dataset)
    # )
    model = torch.hub.load('pytorch/vision:v0.8.0', 'deeplabv3_resnet50', pretrained=True)
    # model = models.segmentation.fcn_resnet101(pretrained=True).eval()

    # Normalization
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    to_image = transforms.ToPILImage()

    # Testing...
    model.eval()
    input_image = Image.open("deeplab.jpg")

    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(input_batch)['out'][0]

    output_predictions = output.argmax(0)
    output = pallette_plot(output_predictions)

    # Loading...
    restart = False
    folder_path = 'data/images/'

    if restart:
        xlsx_file = openpyxl.load_workbook('data/full-data.xlsx')
        sheet = xlsx_file['2022full-info']
        f = open('data/full-info.pickle', 'wb')
        pickle.dump(sheet, f)
        f.close()
    else:
        f = open('data/full-info.pickle', 'rb')
        sheet = pickle.load(f)
        f.close()

    year_list = [2017, 2020]

    num_locations = 10 # in total 53319
    for location_id, _ in enumerate(sheet.iter_rows(max_row=num_locations)):
        if location_id == 0:
            continue

        for year in year_list:
            filename = 'location{}_year{}.png'.format(location_id, year)
            output_filename = 'output/location{}_year{}_out.png'.format(location_id, year)

            img  = Image.open(folder_path + filename).convert('RGB')
            img_torch = preprocess(img).unsqueeze(0)
            # print('input shape', img_torch.shape)
            mask_torch = model(img_torch)['out'][0]
            # print('output shape', mask_torch.shape)
            mask = mask_torch.argmax(0)
            mask_output = pallette_plot(mask)
            plt.imshow(mask_output)
            plt.savefig(folder_path + output_filename)

