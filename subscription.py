import stripe
from functools import wraps
from flask import current_app, jsonify, request
from flask_login import current_user

stripe.api_key = 'your_stripe_test_key'  # Replace with your Stripe key

PRICING_TIERS = {
    'free': {
        'name': 'Free Tier',
        'max_file_size': 50 * 1024 * 1024,  # 50MB
        'features': ['basic_split', 'basic_export'],
        'price': 0
    },
    'premium': {
        'name': 'Premium',
        'max_file_size': 500 * 1024 * 1024,  # 500MB
        'features': ['all_features', 'no_watermark', 'priority_processing'],
        'price': 999,  # $9.99 in cents
        'stripe_price_id': 'your_stripe_price_id'  # Add your Stripe price ID here
    }
}

def check_subscription(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get user's subscription tier
        tier = current_user.subscription_tier
        
        # Check file size if it's an upload request
        if request.method == 'POST' and request.files:
            file = request.files['file']
            file.seek(0, 2)  # Seek to end of file
            size = file.tell()  # Get file size
            file.seek(0)  # Reset file pointer
            
            if size > PRICING_TIERS[tier]['max_file_size']:
                return jsonify({
                    'error': 'File size exceeds plan limit',
                    'upgrade_url': '/pricing'
                }), 413
        
        return f(*args, **kwargs)
    return decorated_function 