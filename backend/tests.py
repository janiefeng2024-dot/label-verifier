from matcher import LabelMatcher

matcher = LabelMatcher()

# ---------------------------
# MOCK DATA
# ---------------------------

VALID_LABEL = """
OLD TOM DISTILLERY
Kentucky Straight Bourbon Whiskey
45% Alc./Vol. (90 Proof)
750 mL
PRODUCT OF USA
GOVERNMENT WARNING: Drinking distilled spirits...
BOTTLED BY OLD TOM DISTILLERY, KY
"""

MISSING_WARNING = """
OLD TOM DISTILLERY
Kentucky Straight Bourbon Whiskey
45% Alc./Vol.
750 mL
PRODUCT OF USA
BOTTLED BY OLD TOM DISTILLERY, KY
"""

INVALID_ABV = """
OLD TOM DISTILLERY
Kentucky Straight Bourbon Whiskey
Forty Five Percent Alcohol
750 mL
PRODUCT OF USA
GOVERNMENT WARNING: Drinking distilled spirits...
BOTTLED BY OLD TOM DISTILLERY, KY
"""

MISSING_NET = """
OLD TOM DISTILLERY
Kentucky Straight Bourbon Whiskey
45% Alc./Vol.
PRODUCT OF USA
GOVERNMENT WARNING: Drinking distilled spirits...
BOTTLED BY OLD TOM DISTILLERY, KY
"""

# ---------------------------
# TEST HELPERS
# ---------------------------

def assert_true(condition, msg):
    if not condition:
        raise AssertionError(msg)

def assert_false(condition, msg):
    if condition:
        raise AssertionError(msg)

# ---------------------------
# TEST CASES
# ---------------------------

def test_valid_label():
    result = matcher.validate(VALID_LABEL)

    assert_true(result["is_valid"], "Valid label should pass")
    assert_true(result["confidence"] > 0.7, "Confidence too low for valid label")
    assert_true(len(result["issues"]) == 0, "Valid label should have no issues")


def test_missing_warning():
    result = matcher.validate(MISSING_WARNING)

    assert_false(result["is_valid"], "Missing warning should fail")
    assert_true("government warning" in str(result["issues"]), "Warning issue not detected")


def test_invalid_abv():
    result = matcher.validate(INVALID_ABV)

    assert_false(result["is_valid"], "Invalid ABV should fail")
    assert_true(any("alcohol" in i.lower() for i in result["issues"]),
                "ABV issue not detected")


def test_missing_net_contents():
    result = matcher.validate(MISSING_NET)

    assert_false(result["is_valid"], "Missing net contents should fail")
    assert_true(any("net" in i.lower() for i in result["issues"]),
                "Net contents issue not detected")


# ---------------------------
# RUNNER
# ---------------------------

if __name__ == "__main__":
    print("Running LabelMatcher tests...\n")

    test_valid_label()
    print("✔ test_valid_label passed")

    test_missing_warning()
    print("✔ test_missing_warning passed")

    test_invalid_abv()
    print("✔ test_invalid_abv passed")

    test_missing_net_contents()
    print("✔ test_missing_net_contents passed")

    print("\n🎉 All tests passed successfully!")