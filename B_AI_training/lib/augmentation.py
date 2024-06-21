# Augmentations
"""
Since our dataset is small we will apply a large number of different augmentations:
 - horizontal flip
 - affine transforms
 - perspective transforms
 - brightness/contrast/colors manipulations
 - image bluring and sharpening
 - gaussian noise
 - random crops

All this transforms can be easily applied with [**Albumentations**](https://github.com/albu/albumentations/) - fast augmentation library.
"""

import albumentations as A
# data_height=480
# data_width=640
def round_clip_0_1(x, **kwargs):
    return x.round().clip(0, 1)

# define heavy augmentations
def get_training_augmentation(data_height,data_width):
    train_transform = [
        A.Resize(data_height,data_width),
        A.HorizontalFlip(p=0.5), # strong augmentation
        # A.HorizontalFlip(p=0.3), # more augmentation
        # weak augmentation

        #A.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),
        A.ShiftScaleRotate(scale_limit=0.1, rotate_limit=10, shift_limit=0, p=0.5, border_mode=0), # strong augmentation
        # A.ShiftScaleRotate(scale_limit=0.4, rotate_limit=10, shift_limit=0.1, p=0.7, border_mode=0), # more augmentation
        # A.ShiftScaleRotate(scale_limit=0.1, rotate_limit=10, shift_limit=0, p=0.3, border_mode=0), # weak augmentation

        # A.PadIfNeeded(min_height=480, min_width=640, always_apply=True, border_mode=0),
        # A.RandomCrop(height=480, width=640, always_apply=True),

        A.IAAAdditiveGaussianNoise(p=0.2),
        
        A.IAAPerspective(p=0.5), # strong augmentation
        # A.IAAPerspective(p=0.4), # more augmentation
        # A.IAAPerspective(p=0.3), # weak augmentation

        A.OneOf(
            [
                A.CLAHE(p=1),
                A.RandomBrightness(p=1),
                A.RandomGamma(p=1),
            ],
            p=0.9, # strong augmentation
            # p=0.8, # more augmentation
            # p=0.3, # weak augmentation
        ),

        A.OneOf(
            [
                A.IAASharpen(p=1),
                A.Blur(blur_limit=3, p=1),
                A.MotionBlur(blur_limit=3, p=1),
            ],
            p=0.9, # strong augmentation
            # p=0.8, # more augmentation
            # p=0.3, # weak augmentation
        ),

        A.OneOf(
            [
                A.RandomContrast(p=1),
                A.HueSaturationValue(p=1),
            ],
            p=0.9, # strong augmentation
            # p=0.8, # more augmentation
            # p=0.3, # weak augmentation
        ),
        A.Lambda(mask=round_clip_0_1)
    ]
    return A.Compose(train_transform)


def get_validation_augmentation(data_height,data_width):
    """Add paddings to make image shape divisible by 32"""
    test_transform = [
        A.Resize(data_height,data_width),
        A.RandomCrop(height=data_height, width=data_width, always_apply=True),
        A.PadIfNeeded(data_height, data_width)
    ]
    return A.Compose(test_transform)

def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform
    
    Args:
        preprocessing_fn (callbale): data normalization function 
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    
    """
    
    _transform = [
        A.Lambda(image=preprocessing_fn),
    ]
    return A.Compose(_transform)