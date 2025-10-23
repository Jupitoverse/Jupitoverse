# 🚀 Wix Deployment Guide for Jupitoverse

This guide will help you embed your Jupitoverse features into your Wix website (www.jupitoverse.com).

## 📋 Quick Start

All HTML files are **single-page applications** designed to be easily embedded into Wix. You have two main options:

### Option 1: HTML Embed (Recommended)
### Option 2: External Hosting + iFrame

---

## Method 1: Direct HTML Embed

### Step-by-Step Instructions:

#### 1. **Open Wix Editor**
   - Go to www.wix.com and open your website editor
   - Navigate to the page where you want to add the feature

#### 2. **Add HTML Embed Element**
   - Click the **"+"** button to add elements
   - Go to **"Embed"** → **"Custom Embeds"** → **"HTML iframe"** or **"HTML Embed"**

#### 3. **Copy HTML Content**
   - Open the desired HTML file (e.g., `Atom_Simulator.html`)
   - Select all content (Ctrl+A or Cmd+A)
   - Copy (Ctrl+C or Cmd+C)

#### 4. **Paste into Wix**
   - In the Wix editor, click the HTML embed element
   - Click **"Enter Code"**
   - Paste your HTML content
   - Click **"Update"**

#### 5. **Adjust Size**
   - Resize the embed element to fit your page
   - Recommended sizes:
     - **Simulators**: 1200px wide × 800px tall
     - **Blog/Events**: 1400px wide × full height
     - **AI Repository**: 1600px wide × full height
     - **Tutorials**: 1400px wide × full height

---

## Method 2: External Hosting + iFrame

If HTML embed has size limitations, use external hosting:

### Step 1: Upload to External Host

**Option A: GitHub Pages (Free)**
1. Create a GitHub repository
2. Upload all HTML files
3. Enable GitHub Pages in Settings
4. Access via: `https://yourusername.github.io/jupitoverse/`

**Option B: Netlify (Free)**
1. Go to netlify.com
2. Drag and drop the Jupitoverse folder
3. Get your site URL (e.g., `https://jupitoverse.netlify.app`)

**Option C: Vercel (Free)**
1. Go to vercel.com
2. Import the project
3. Deploy and get URL

### Step 2: Embed in Wix using iFrame

```html
<iframe 
  src="https://your-hosted-url.com/index.html" 
  width="100%" 
  height="800px"
  frameborder="0"
  allowfullscreen>
</iframe>
```

---

## 📄 Page-by-Page Recommendations

### 🏠 **Landing Page** (`index.html`)
- **Best as**: Main homepage or dedicated section
- **Wix Method**: Full page embed or strip
- **Height**: Full viewport (100vh)

### ⚛️ **Atom Simulator** (`Simulation/Atom_Simulator.html`)
- **Best as**: Dedicated tab or section
- **Wix Method**: HTML embed element
- **Recommended Size**: 1200px × 700px
- **Tip**: Works great in a lightbox/popup

### 🌌 **Asteroid Simulator** (`Simulation/Asteroid_Simulator.html`)
- **Best as**: Dedicated tab or section
- **Wix Method**: HTML embed element
- **Recommended Size**: 1200px × 750px
- **Note**: Interactive panning requires space

### 📅 **Science Events** (`Science_Events.html`)
- **Best as**: Full page or large section
- **Wix Method**: Full-width embed
- **Recommended Size**: 1400px × 1000px
- **Tip**: Enable scrolling within embed

### 💼 **Job Portal** (`Science_Jobs.html`)
- **Best as**: Full dedicated page
- **Wix Method**: Full page embed
- **Recommended Size**: 1400px × full height
- **Tip**: Make sure filters are visible

### 📚 **Blog** (`Science_Blog.html`)
- **Best as**: Blog section or separate page
- **Wix Method**: Full page embed
- **Recommended Size**: 1200px × full height
- **Note**: Articles expand, so allow scrolling

### 🚀 **Projects** (`Projects_Showcase.html`)
- **Best as**: Portfolio/Projects page
- **Wix Method**: Full page embed
- **Recommended Size**: 1400px × full height

### 🤖 **AI Repository** (`AI_Repository.html`)
- **Best as**: Resources section
- **Wix Method**: Full page embed
- **Recommended Size**: 1600px × full height
- **Tip**: Search bar needs to be accessible

### 🎓 **Tutorials** (`Tutorials.html`)
- **Best as**: Learning/Education page
- **Wix Method**: Full page embed with sidebar
- **Recommended Size**: 1400px × full height
- **Important**: Sidebar navigation must be visible

---

## 🎨 Styling Tips for Wix Integration

### 1. **Background Matching**
   - Most pages have dark backgrounds
   - Set Wix page background to match (usually black or dark blue)

### 2. **Remove Wix Header/Footer**
   - For full-page embeds, consider hiding Wix header/footer
   - Creates seamless experience

### 3. **Mobile Optimization**
   - All pages are responsive
   - Test on mobile preview in Wix
   - Adjust embed sizes for mobile breakpoints

### 4. **Loading Performance**
   - HTML embeds load fast since they're self-contained
   - No external dependencies to slow down

---

## 🔗 Creating Navigation in Wix

### Option 1: Menu Items
Add these to your Wix navigation menu:
- Home
- Simulators → Atom Simulator, Asteroid Simulator
- Events
- Jobs
- Blog
- Projects
- AI Tools
- Tutorials

### Option 2: Landing Page with Links
Use `index.html` as your landing page with built-in navigation to all features.

---

## ⚡ Pro Tips

### 1. **Test in Preview Mode**
   - Always preview before publishing
   - Test all interactive features
   - Check mobile responsiveness

### 2. **Keep Files Updated**
   - When you update HTML files, simply re-embed
   - Wix caches embeds, so clear cache if needed

### 3. **Performance Optimization**
   - Don't embed all pages on one Wix page
   - Use separate pages/sections for each feature
   - This keeps load times fast

### 4. **Cross-Browser Testing**
   - Test in Chrome, Firefox, Safari, Edge
   - All features are compatible

### 5. **Analytics Integration**
   - Add Google Analytics to track usage
   - Insert tracking code in each HTML file

---

## 🐛 Troubleshooting

### Problem: Embed appears blank
**Solution**: 
- Check if HTML was fully copied
- Ensure no special characters were lost
- Try refreshing the Wix editor

### Problem: Interactive features don't work
**Solution**:
- Make sure you used "HTML Embed" not just "Text"
- Wix must allow JavaScript execution
- Check if scripts are enabled in embed settings

### Problem: Size issues on mobile
**Solution**:
- Each page is responsive by default
- Adjust Wix embed settings for mobile
- Test with Wix mobile preview tool

### Problem: Scrolling doesn't work
**Solution**:
- Enable scrolling in iFrame settings
- Set appropriate height for content
- Use `overflow: auto` in embed container

---

## 📱 Mobile Optimization Checklist

- [ ] Test all embeds on mobile preview
- [ ] Ensure touch interactions work (simulators)
- [ ] Check that text is readable (minimum 16px)
- [ ] Verify navigation menus are accessible
- [ ] Test forms and search functionality
- [ ] Confirm buttons are large enough to tap
- [ ] Check page load speed on 3G/4G

---

## 🎯 Recommended Site Structure

```
Your Wix Site
├── Home (index.html - Landing Page)
├── Simulations
│   ├── Atom Simulator
│   └── Asteroid Simulator
├── Events
├── Jobs
├── Blog
├── Projects
├── AI Tools
└── Learn (Tutorials)
```

---

## 🔒 Security Notes

- All pages are client-side only (no backend)
- No user data is collected or stored
- Safe to embed without security concerns
- No external API calls that could fail

---

## 📊 Analytics Setup (Optional)

To track usage, add this to each HTML file before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

---

## ✅ Final Checklist Before Going Live

- [ ] All HTML files tested in browser
- [ ] Each page embedded in Wix
- [ ] Navigation menu created
- [ ] Mobile responsiveness verified
- [ ] All links working
- [ ] Interactive features functional
- [ ] Wix site published
- [ ] Cross-browser testing completed
- [ ] Performance optimized
- [ ] Analytics installed (if desired)

---

## 🎉 Success!

Once deployed, your Jupitoverse site will be:
- ✨ Fully interactive
- 📱 Mobile-friendly
- ⚡ Fast-loading
- 🎨 Beautiful
- 🔬 Educational
- 🚀 Professional

---

## 📞 Need Help?

If you encounter issues:
1. Check Wix documentation on HTML embeds
2. Verify browser console for errors (F12)
3. Test in incognito mode
4. Clear Wix editor cache

**Built with ❤️ for www.jupitoverse.com**

*Your science communication journey starts here!*

