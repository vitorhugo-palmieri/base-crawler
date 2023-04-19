def change_flag_reprocessed_to_true(transformed_item):
    transformed_item["metadata"]["reprocessed"] = True
    return transformed_item
