# Ground News Scraper 🌍📰

A powerful web scraping tool for extracting comprehensive news data from Ground.news articles, designed for media bias analysis and research purposes.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Overview

Ground News Scraper is a comprehensive tool that extracts detailed information from Ground.news articles, including:
- **Political bias distributions** across news sources
- **Perspective summaries** from left, center, and right viewpoints
- **Source metadata** with bias classifications
- **Article content** and publication details

Perfect for researchers, journalists, and data analysts studying media bias and news coverage patterns.

## ✨ Features

### 🔍 Data Extraction
- **Multi-perspective Analysis**: Extracts left, center, and right political viewpoints
- **Source Tracking**: Collects information from all news sources covering a story
- **Bias Classification**: Captures bias ratings for each source
- **Comprehensive Metadata**: Article titles, URLs, timestamps, and source counts

### 🖥️ User Interfaces
- **GUI Application**: User-friendly tkinter interface for easy interaction
- **Command Line**: Direct script execution for automation and batch processing
- **Real-time Progress**: Live console output and progress tracking

### 📊 Data Management
- **JSON Storage**: Structured data saved in JSON format for easy processing
- **Unique Story IDs**: Automatic generation of unique identifiers for each article
- **Data Analysis Tools**: Built-in scripts for analyzing collected data

## 🏗️ Project Structure

```
GN_fetch/
├── g.py                    # Main scraper engine (Selenium-based)
├── gui.py                  # GUI application interface
├── a.py                    # Data analysis and processing tool
├── json/                   # Directory for scraped data
│   ├── GN_20250820_*.json  # Individual article data files
│   └── ...
└── data/                   # Additional data storage
```

## 🚀 Quick Start

### Prerequisites

```bash
# Required Python packages
pip install selenium
pip install webdriver-manager
pip install tkinter  # Usually included with Python
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sakhadib/Ground-News-Scraper.git
   cd Ground-News-Scraper
   ```

2. **Install dependencies**
   ```bash
   pip install selenium webdriver-manager
   ```

3. **Run the application**
   ```bash
   # GUI Interface
   python gui.py
   
   # Command Line Interface
   python g.py "https://ground.news/article/your-article-url"
   ```

## 💻 Usage

### GUI Application

1. **Launch the GUI**
   ```bash
   python gui.py
   ```

2. **Enter Ground.news URL** in the input field

3. **Click "Fetch Data"** to start scraping

4. **Monitor progress** in the console output

5. **Access results** in the `json/` directory

### Command Line Interface

```bash
# Basic usage
python g.py "https://ground.news/article/your-article-url"

# The script will automatically:
# - Launch Chrome browser
# - Navigate to the article
# - Extract all data points
# - Save results to json/ directory
```

### Data Analysis

```bash
# Analyze collected data
python a.py

# Enter the path to your json/ directory when prompted
# View bias distribution statistics and source counts
```

## 📋 Data Structure

Each scraped article generates a JSON file with the following structure:

```json
{
  "story_id": "GN_20250820_abc12345",
  "metadata": {
    "title": "Article Title",
    "timestamp": "2025-08-20T21:33:02.620020",
    "url": "https://ground.news/article/..."
  },
  "bias_distribution": {
    "total_sources": "134",
    "leaning_left": "18",
    "center": "21",
    "leaning_right": "15"
  },
  "perspective_summaries": {
    "left": ["Left perspective point 1", "..."],
    "center": ["Center perspective point 1", "..."],
    "right": ["Right perspective point 1", "..."]
  },
  "sources": [
    {
      "news_title": "Source Article Title",
      "news_link": "https://source-url.com",
      "bias": "Lean Right",
      "source_name": "Source Name"
    }
  ]
}
```

## 🔧 Technical Details

### Core Components

#### `g.py` - Main Scraper Engine
- **Selenium WebDriver**: Automated browser interaction
- **XPath Extraction**: Precise element targeting
- **Dynamic Loading**: Handles "Load More" functionality
- **Error Handling**: Robust exception management
- **Chrome Driver**: Automatic driver management

#### `gui.py` - Graphical Interface
- **Tkinter Framework**: Cross-platform GUI
- **Threading**: Non-blocking UI operations
- **Real-time Logging**: Live progress updates
- **Input Validation**: URL format checking
- **Process Management**: Start/stop controls

#### `a.py` - Data Analysis
- **JSON Processing**: Multi-encoding support
- **Statistical Analysis**: Bias distribution calculations
- **Data Aggregation**: Cross-article summaries
- **Error Recovery**: Handles corrupted files

### Browser Automation Features

- **Maximized Window**: Ensures element visibility
- **Explicit Waits**: Reliable element loading
- **Action Chains**: Complex user interactions
- **Dynamic Content**: Handles JavaScript-loaded content
- **Element Clicking**: Automated perspective switching

## 📊 Use Cases

### Research Applications
- **Media Bias Studies**: Analyze coverage patterns across political spectrum
- **Source Diversity Analysis**: Track source representation in news stories
- **Temporal Analysis**: Study how coverage changes over time
- **Comparative Studies**: Compare bias distributions across topics

### Data Science Projects
- **Machine Learning**: Train models on bias-labeled news data
- **Natural Language Processing**: Analyze perspective-based text differences
- **Network Analysis**: Study source relationships and citation patterns
- **Visualization**: Create bias distribution charts and graphs

### Journalism Tools
- **Source Verification**: Cross-reference multiple news sources
- **Bias Awareness**: Understand perspective diversity in coverage
- **Story Tracking**: Monitor how stories develop across sources
- **Research Assistance**: Gather comprehensive source lists

## ⚠️ Important Notes

### Ethical Usage
- **Respect robots.txt**: Follow Ground.news terms of service
- **Rate Limiting**: Don't overwhelm servers with requests
- **Academic Use**: Primarily intended for research purposes
- **Data Attribution**: Credit Ground.news as data source

### Technical Considerations
- **Chrome Dependency**: Requires Chrome browser installation
- **Internet Connection**: Stable connection needed for scraping
- **File Permissions**: Ensure write access to json/ directory
- **Memory Usage**: Large datasets may require substantial RAM

### Limitations
- **Dynamic Content**: Some elements may load differently
- **Site Changes**: XPath selectors may need updates if site structure changes
- **JavaScript Requirements**: Requires enabled JavaScript for full functionality
- **Rate Limits**: May encounter rate limiting with excessive requests

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution
- **Error Handling**: Improve robustness
- **Data Export**: Add CSV/Excel export options
- **Visualization**: Create data visualization tools
- **Performance**: Optimize scraping speed
- **Documentation**: Enhance code documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ground.news**: For providing comprehensive news bias analysis
- **Selenium Project**: For powerful web automation capabilities
- **Chrome DevTools**: For XPath development and debugging
- **Python Community**: For excellent libraries and documentation

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/sakhadib/Ground-News-Scraper/issues)
- **Documentation**: Check this README and code comments
- **Community**: Join discussions in the Issues section

## 🔮 Future Enhancements

- **API Integration**: Direct Ground.news API support (if available)
- **Batch Processing**: Multiple URL processing
- **Export Options**: CSV, Excel, and database export
- **Scheduling**: Automated periodic scraping
- **Advanced Analytics**: Built-in statistical analysis tools
- **Docker Support**: Containerized deployment option

---

**Happy Scraping! 🚀**

*Remember to use this tool responsibly and in accordance with Ground.news terms of service.*
