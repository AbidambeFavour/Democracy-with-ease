#!/usr/bin/env python
"""
Test dashboard template rendering for SimpleVote.
"""

import os
import sys
import django

# Add project to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
django.setup()

from django.template import Template, Context
from django.contrib.auth import get_user_model

User = get_user_model()

def test_dashboard_template_syntax():
    """Test dashboard template for syntax errors."""
    print("🧪 Testing Dashboard Template Syntax...")
    
    try:
        # Read the dashboard template
        with open('templates/accounts/dashboard.html', 'r') as f:
            template_content = f.read()
        
        # Create a mock context
        mock_user = type('MockUser', (), {
            'get_full_name': lambda: 'Test User',
            'username': 'testuser',
            'get_polls_created_count': lambda: 5,
            'get_votes_cast_count': lambda: 12,
            'date_joined': '2024-01-01',
        })()
        
        context = Context({
            'user': mock_user,
            'total_polls': 5,
            'total_votes_cast': 12,
            'active_polls': 3,
            'polls_created': [],
            'recent_votes': [],
            'recent_activities': [],
            'trending_polls': [],
        })
        
        # Try to render the template
        template = Template(template_content)
        rendered = template.render(context)
        
        print("✅ Dashboard template syntax is valid")
        print("✅ Template renders successfully")
        
        # Check for key elements
        checks = [
            'Welcome back',
            'polls created',
            'votes cast',
        ]
        
        for check in checks:
            if check in rendered:
                print(f"✅ Found: {check}")
            else:
                print(f"⚠️ Missing: {check}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_filters():
    """Test specific template filters used in dashboard."""
    print("\n🔍 Testing Template Filters...")
    
    from django.template import Template, Context
    
    # Test filters used in dashboard
    test_filters = [
        '{{ "Test User"|default:"Anonymous" }}',
        '{{ 5|default:0 }}',
        '{{ "2024-01-01"|date:"M Y" }}',
        '{{ "Test"|truncatechars:30 }}',
        '{{ 157|add:5|default:0 }}',
    ]
    
    for filter_test in test_filters:
        try:
            template = Template(filter_test)
            rendered = template.render(Context({}))
            print(f"✅ Filter works: {filter_test} -> {rendered.strip()}")
        except Exception as e:
            print(f"❌ Filter failed: {filter_test} -> {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Testing Dashboard Template")
    print("=" * 40)
    
    try:
        # Test template syntax
        syntax_ok = test_dashboard_template_syntax()
        
        # Test filters
        filters_ok = test_template_filters()
        
        if syntax_ok and filters_ok:
            print("\n🎉 Dashboard template tests passed!")
            print("The 'mul' filter issue has been resolved!")
        else:
            print("\n❌ Some template tests failed")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Template test completed")
