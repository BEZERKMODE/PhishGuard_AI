from ml.feature_engineering import extract_features_from_url


def test_feature_extraction():
    url = "http://paypal-login-security-alert-example.com/verify"
    features = extract_features_from_url(url)
    assert features["url_length"] > 0
    assert "suspicious_keyword_count" in features
