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

layer = img[find_layer(img)]
print("ANS...")
print((layer == 1).sum() * (layer == 2).sum())

