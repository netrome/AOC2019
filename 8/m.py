import torch

def get_image(shape, digits):
    rows = tuple(map(tuple, zip(*[iter(digits)] * shape[0])))
    image = tuple(map(tuple, zip(*[iter(rows)] * shape[1])))
    return torch.tensor(image)


img = get_image((25, 6), tuple(map(int, open("in").read().strip())))

def find_layer(image):
    best = 1e10
    best_idx = 0
    for idx, layer in enumerate(image):
        n_zeros = (layer == 0).sum()
        if n_zeros < best:
            best = n_zeros
            best_idx = idx
    return best_idx

def find_color(values):
    idx = 0
    val = 2
    while val == 2:
        val = values[idx]
        idx += 1
    return int(val)

def final_image(image):
    image = image.transpose(0, 1)
    image = image.transpose(1, 2)

    out_img = torch.zeros(image[:, :, 0].shape).long()

    for row in range(out_img.shape[0]):
        for col in range(out_img.shape[1]):
            out_img[row, col] = find_color(image[row, col])

    return out_img

layer = img[find_layer(img)]
print("ANS...")
print((layer == 1).sum() * (layer == 2).sum())

print(img.shape)
print(final_image(img))
print(final_image(img).shape)

print("\n".join(map(lambda row: "".join(map(lambda i: "." if i == 0 else "#", row)), final_image(img))))
