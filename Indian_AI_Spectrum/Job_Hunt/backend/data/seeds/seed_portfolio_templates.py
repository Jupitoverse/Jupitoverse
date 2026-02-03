"""
Seed Portfolio Templates Data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import get_db, PortfolioTemplate, PortfolioTemplateCategory

PORTFOLIO_TEMPLATES = [
    {
        "name": "Developer Dark",
        "slug": "developer-dark",
        "description": "Modern dark theme with smooth animations. Perfect for developers who love the terminal aesthetic.",
        "category": PortfolioTemplateCategory.DEVELOPER,
        "tags": ["dark", "modern", "animated", "developer"],
        "features": ["dark_mode", "smooth_animations", "responsive", "skill_bars", "project_cards"],
        "is_free": True,
        "is_featured": True,
        "display_order": 1,
        "color_schemes": [
            {"name": "Purple Night", "primary": "#6366f1", "secondary": "#8b5cf6", "background": "#0f0f23"},
            {"name": "Cyber Green", "primary": "#10b981", "secondary": "#34d399", "background": "#0d1117"},
            {"name": "Ocean Blue", "primary": "#3b82f6", "secondary": "#60a5fa", "background": "#0a0a1a"}
        ]
    },
    {
        "name": "Minimal Light",
        "slug": "minimal-light",
        "description": "Clean and professional light theme. Focus on content with elegant typography.",
        "category": PortfolioTemplateCategory.GENERAL,
        "tags": ["light", "minimal", "clean", "professional"],
        "features": ["clean_layout", "typography_focus", "responsive", "print_friendly"],
        "is_free": True,
        "is_featured": True,
        "display_order": 2,
        "color_schemes": [
            {"name": "Classic White", "primary": "#2563eb", "secondary": "#3b82f6", "background": "#ffffff"},
            {"name": "Warm Cream", "primary": "#d97706", "secondary": "#f59e0b", "background": "#fefce8"},
            {"name": "Cool Gray", "primary": "#6366f1", "secondary": "#8b5cf6", "background": "#f8fafc"}
        ]
    },
    {
        "name": "Gradient Modern",
        "slug": "gradient-modern",
        "description": "Bold gradient backgrounds with modern card layouts. Stand out from the crowd.",
        "category": PortfolioTemplateCategory.DESIGNER,
        "tags": ["gradient", "modern", "colorful", "bold"],
        "features": ["gradient_backgrounds", "card_animations", "floating_elements", "responsive"],
        "is_free": True,
        "is_featured": True,
        "display_order": 3,
        "color_schemes": [
            {"name": "Purple Sunset", "primary": "#667eea", "secondary": "#764ba2", "background": "gradient"},
            {"name": "Ocean Breeze", "primary": "#4facfe", "secondary": "#00f2fe", "background": "gradient"},
            {"name": "Warm Glow", "primary": "#f093fb", "secondary": "#f5576c", "background": "gradient"}
        ]
    },
    {
        "name": "Terminal Style",
        "slug": "terminal-style",
        "description": "Inspired by command-line interfaces. Show your love for the terminal.",
        "category": PortfolioTemplateCategory.DEVELOPER,
        "tags": ["terminal", "hacker", "retro", "developer"],
        "features": ["typing_animation", "command_prompts", "monospace_font", "matrix_effect"],
        "is_free": True,
        "is_featured": False,
        "display_order": 4,
        "color_schemes": [
            {"name": "Matrix Green", "primary": "#00ff00", "secondary": "#00cc00", "background": "#0c0c0c"},
            {"name": "Amber Retro", "primary": "#ffb000", "secondary": "#ff8c00", "background": "#1a1a1a"},
            {"name": "Cyan Cyber", "primary": "#00ffff", "secondary": "#00d4d4", "background": "#0d1117"}
        ]
    },
    {
        "name": "Glassmorphism",
        "slug": "glassmorphism",
        "description": "Trendy glass-like translucent elements with backdrop blur effects.",
        "category": PortfolioTemplateCategory.DESIGNER,
        "tags": ["glass", "blur", "modern", "trendy"],
        "features": ["glass_effect", "backdrop_blur", "floating_cards", "smooth_animations"],
        "is_free": False,
        "is_premium": True,
        "price": 299,
        "is_featured": True,
        "display_order": 5,
        "color_schemes": [
            {"name": "Aurora", "primary": "#a855f7", "secondary": "#3b82f6", "background": "gradient"},
            {"name": "Sunset", "primary": "#f97316", "secondary": "#ec4899", "background": "gradient"},
            {"name": "Northern Lights", "primary": "#22d3ee", "secondary": "#a855f7", "background": "gradient"}
        ]
    },
    {
        "name": "Creative Portfolio",
        "slug": "creative-portfolio",
        "description": "Bold and creative design for designers and artists. Showcase your personality.",
        "category": PortfolioTemplateCategory.DESIGNER,
        "tags": ["creative", "bold", "artistic", "colorful"],
        "features": ["masonry_layout", "hover_effects", "custom_cursor", "scroll_animations"],
        "is_free": False,
        "is_premium": True,
        "price": 399,
        "is_featured": False,
        "display_order": 6,
        "color_schemes": [
            {"name": "Vibrant", "primary": "#ff6b6b", "secondary": "#feca57", "background": "#ffffff"},
            {"name": "Pop Art", "primary": "#ff00ff", "secondary": "#00ffff", "background": "#000000"},
            {"name": "Pastel Dreams", "primary": "#ddd6fe", "secondary": "#fecaca", "background": "#faf5ff"}
        ]
    },
    {
        "name": "Data Scientist",
        "slug": "data-scientist",
        "description": "Showcase your ML projects, visualizations, and research. Built for data professionals.",
        "category": PortfolioTemplateCategory.DATA_SCIENCE,
        "tags": ["data", "ml", "charts", "professional"],
        "features": ["chart_integration", "notebook_embeds", "metric_cards", "publication_section"],
        "is_free": True,
        "is_featured": False,
        "display_order": 7,
        "color_schemes": [
            {"name": "Jupyter", "primary": "#f37626", "secondary": "#ff8c42", "background": "#ffffff"},
            {"name": "Analytics Blue", "primary": "#1a73e8", "secondary": "#4285f4", "background": "#f8f9fa"},
            {"name": "Deep Learning", "primary": "#7c3aed", "secondary": "#a78bfa", "background": "#18181b"}
        ]
    },
    {
        "name": "Product Manager",
        "slug": "product-manager",
        "description": "Highlight your product launches, case studies, and impact metrics.",
        "category": PortfolioTemplateCategory.PRODUCT,
        "tags": ["product", "case-study", "metrics", "professional"],
        "features": ["case_study_layout", "metric_highlights", "timeline_view", "testimonials"],
        "is_free": True,
        "is_featured": False,
        "display_order": 8,
        "color_schemes": [
            {"name": "Corporate", "primary": "#2563eb", "secondary": "#3b82f6", "background": "#ffffff"},
            {"name": "Startup", "primary": "#059669", "secondary": "#10b981", "background": "#f0fdf4"},
            {"name": "Enterprise", "primary": "#1e40af", "secondary": "#3b82f6", "background": "#eff6ff"}
        ]
    },
    {
        "name": "Neomorphism",
        "slug": "neomorphism",
        "description": "Soft UI design with subtle shadows creating a 3D-like appearance.",
        "category": PortfolioTemplateCategory.GENERAL,
        "tags": ["soft-ui", "3d", "subtle", "modern"],
        "features": ["soft_shadows", "rounded_elements", "tactile_buttons", "depth_effect"],
        "is_free": False,
        "is_premium": True,
        "price": 299,
        "is_featured": False,
        "display_order": 9,
        "color_schemes": [
            {"name": "Soft Gray", "primary": "#6366f1", "secondary": "#8b5cf6", "background": "#e0e5ec"},
            {"name": "Warm Stone", "primary": "#d97706", "secondary": "#f59e0b", "background": "#f5f0e6"},
            {"name": "Cool Blue", "primary": "#0ea5e9", "secondary": "#38bdf8", "background": "#e0f2fe"}
        ]
    },
    {
        "name": "3D Interactive",
        "slug": "3d-interactive",
        "description": "Three.js powered 3D elements and interactive backgrounds.",
        "category": PortfolioTemplateCategory.DEVELOPER,
        "tags": ["3d", "interactive", "threejs", "immersive"],
        "features": ["3d_background", "particle_effects", "interactive_elements", "webgl"],
        "is_free": False,
        "is_premium": True,
        "price": 499,
        "is_featured": True,
        "display_order": 10,
        "color_schemes": [
            {"name": "Space", "primary": "#8b5cf6", "secondary": "#ec4899", "background": "#030712"},
            {"name": "Neon", "primary": "#22d3ee", "secondary": "#f472b6", "background": "#0f172a"},
            {"name": "Galactic", "primary": "#6366f1", "secondary": "#f97316", "background": "#020617"}
        ]
    }
]


def seed_portfolio_templates():
    """Seed portfolio templates"""
    db = next(get_db())
    
    try:
        for template_data in PORTFOLIO_TEMPLATES:
            existing = db.query(PortfolioTemplate).filter(
                PortfolioTemplate.slug == template_data["slug"]
            ).first()
            
            if existing:
                print(f"Template exists: {template_data['name']}")
                continue
            
            template = PortfolioTemplate(
                name=template_data["name"],
                slug=template_data["slug"],
                description=template_data["description"],
                category=template_data["category"],
                tags=template_data["tags"],
                features=template_data["features"],
                color_schemes=template_data["color_schemes"],
                is_free=template_data.get("is_free", True),
                is_premium=template_data.get("is_premium", False),
                price=template_data.get("price", 0),
                is_featured=template_data.get("is_featured", False),
                display_order=template_data["display_order"]
            )
            db.add(template)
            print(f"Created template: {template_data['name']}")
        
        db.commit()
        print("✅ Portfolio templates seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding templates: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_portfolio_templates()
