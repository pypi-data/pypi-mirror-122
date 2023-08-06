from pathlib import Path
from subprocess import check_call
from time import time

from .logger import logger

def get_imagestack_info(task_info):
    """
    Reads the source_format from the task information (parse with
    task.get_task_info).

    Returns a dictionary with the following information:

    >>> { 'image_type': 'jp2' or 'jpg' or 'tif', 'archive_type': 'zip' or 'tar'. }
    """
    source_format = task_info['sourceFormat']
    if source_format == 'Single Page Processed JP2 ZIP':
        return {'image_type': 'jp2', 'archive_type': 'zip'}
    if source_format == 'Single Page Processed JP2 Tar':
        return {'image_type': 'jp2', 'archive_type': 'tar'}
    if source_format == 'Single Page Processed JPEG ZIP':
        return {'image_type': 'jpg', 'archive_type': 'zip'}
    if source_format == 'Single Page Processed JPEG Tar':
        return {'image_type': 'jpg', 'archive_type': 'tar'}
    if source_format == 'Single Page Processed TIFF ZIP':
        return {'image_type': 'tif', 'archive_type': 'zip'}
    if source_format == 'Single Page Processed TIFF Tar':
        return {'image_type': 'tif', 'archive_type': 'tar'}
    raise Exception('Unhandled imagestack format: %s' % source_format)


def unpack_and_validate_imagestack(imagestack_path, imagestack_info, dst):
    """Unpack and validate an imagestack

    An imagestack is valid if it contains at least one directory that contains
    at least one image of the expected image type.

    Args:

    * imagestack_path (``str``): The imagestack archive path
    * imagestack_info (``dict``)::

        >>> {'archive_type': ..., 'image_type': ...}

    * dst (``str``): Destination directory for the unpacked imagestack

    Returns:

    * ``(str, int)``: Tuple containing the path to the unpacked image directory
                      and the image count.
    """
    logger.info('Unpacking image stack.')
    start_time = time()
    if imagestack_info['archive_type'] == 'tar':
        check_call(['tar', '-xf', imagestack_path, '-C', dst])
    elif imagestack_info['archive_type'] == 'zip':
        check_call(['unzip', '-qq', '-o', imagestack_path, '-d', dst])
    else:
        raise ValueError('Cannot extract archive_type %s' % imagestack_info['archive_type'])
    logger.info('Unpacking image stack took %f seconds', time() - start_time)

    for f in Path(dst).iterdir():
        if f.name.endswith(f'_{imagestack_info["image_type"]}'):
            img_dir = f
            break
    else:
        raise Exception('Unable to locate image directory in imagestack.')

    image_count = 0
    for img_path in img_dir.iterdir():
        if img_path.suffix[1:] == imagestack_info['image_type']:
            image_count += 1

    if image_count == 0:
        raise Exception('Imagestack contains no valid images.')

    return str(img_dir), image_count

# TODO: function to unpack an image stack

# TODO: function to iterate over images in an image stack
