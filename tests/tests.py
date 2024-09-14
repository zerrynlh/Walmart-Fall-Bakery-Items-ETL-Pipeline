import unittest
from scripts.utils import 
    print_dict_keys,
    extract_data,
    replace_li,
    safe_convert_price,
    extract_weight,
    transform_data
import pandas as pd
import json

class TestUtils(unittest.TestCase):

    def test_replace_li(self):
        # Test HTML list item replacement
        html_desc = "<li>Item 1</li> <li>Item 2</li>"
        expected = "Item 1 Item 2"
        result = replace_li(html_desc)
        self.assertEqual(result, expected)

    def test_safe_convert_price(self):
        # Test price conversion
        price_str = "$1,234.56"
        expected = 1234.56
        result = safe_convert_price(price_str)
        self.assertEqual(result, expected)
        
        # Test invalid price string
        invalid_price_str = "invalid"
        expected = None
        result = safe_convert_price(invalid_price_str)
        self.assertEqual(result, expected)

    def test_extract_weight(self):
        # Test weight extraction
        desc = "Delicious cake, weight 12 OZ"
        expected = 12.0
        result = extract_weight(desc)
        self.assertEqual(result, expected)
        
        # Test weight extraction with no weight
        desc_no_weight = "Delicious cake"
        expected = None
        result = extract_weight(desc_no_weight)
        self.assertEqual(result, expected)

    def test_transform_data(self):
        # Mock data
        fall_data = [
            {
                'priceInfo': {'linePrice': '$1,234.56'},
                'name': 'Cake A',
                'shortDescription': '<li>Delicious</li> <li>Sweet</li>',
                'rating': {'averageRating': 4.5, 'numberOfReviews': 10}
            },
            {
                'priceInfo': {'linePrice': '$789.10'},
                'name': 'Cake B',
                'shortDescription': '<li>Fresh</li>',
                'rating': {'averageRating': 4.0, 'numberOfReviews': 5}
            }
        ]
        expected_df = pd.DataFrame({
            'TITLE': ['Cake A', 'Cake B'],
            'PRICE': [1234.56, 789.10],
            'DESCRIPTION': ['Delicious Sweet', 'Fresh'],
            'WEIGHT': [None, None],  # No weight info in mock data
            'RATING': [4.5, 4.0],
            'NumReviews': [10, 5]
        }).rename(columns={'NumReviews': 'NUM_REVIEWS'})

        result_df = transform_data(fall_data)
        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == '__main__':
    unittest.main()