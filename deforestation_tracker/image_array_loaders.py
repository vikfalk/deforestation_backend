from deforestation_tracker.sentinelhub_requester import search_available_L2A_tiles, request_image, sentinelhub_authorization, box_from_point
from deforestation_tracker.utils import timeframe_constructor
from PIL import Image
import numpy as np

def load_img_array_from_satellite(
        lat_deg: float = -8.48638,
        lon_deg: float = -55.26209,
        date: str = "2024-05-30",
        request_type: str = "TrueColor") -> np.array:
    """Loads a satellite image array from sentinel hub, scales it and returns it."""


    # time_interval_6m = timeframe_constructor(date, temporal_padding=91)

    box_ = box_from_point(lat_deg=lat_deg, lon_deg=lon_deg, image_size_px=512, resolution_m_per_px=10)

    # Authorize session
    config_, catalog_ = sentinelhub_authorization()

    # Search for tiles
    #to_be_logged = (f"Searching for in {box_} on date: {date}")
    optimal_tile = search_available_L2A_tiles(catalog=catalog_, bbox=box_, date_request=date, range_days=91, maxCloudCoverage=10)
    if optimal_tile:
        # Request tile
        img_array = request_image(
            box=box_, time_interval=(optimal_tile.get('date'), optimal_tile.get('date')), config=config_,
            image_size_px=512, resolution_m_per_px=10,  request_type=request_type
        )
        #to_be_logged = (f"found optimal tile with penalty of {optimal_tile.get('penalty')}. Shape: {img_array.shape}, Mean: {img_array.flatten().mean()}")
        return img_array, optimal_tile.get('date')
    else:
        #to_be_logged = (f"no tiles found for {date} plus/minus 3 months with less than 10% Clouds.")
        return None, None

# img_array, request_info = load_img_array_from_satellite()
# print(request_info)

# print(load_img_array_from_satellite(date="2018-06-01"))
print(load_img_array_from_satellite(date="2022-05-31"))
# print(load_img_array_from_satellite(date="2024-05-20"))
# print(load_img_array_from_satellite(date="2023-06-20"))
