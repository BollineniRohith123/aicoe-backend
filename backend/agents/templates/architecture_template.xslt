<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <!-- Main template -->
    <xsl:template match="/systemArchitecture">
        <html lang="en">
        <head>
            <meta charset="UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>System Architecture</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }
                .header {
                    background: linear-gradient(135deg, #dc2626, #ef4444);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }
                .section {
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .section h2 {
                    color: #dc2626;
                    border-bottom: 2px solid #ef4444;
                    padding-bottom: 10px;
                    margin-top: 0;
                }
                .diagram-container {
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 20px 0;
                    text-align: center;
                }
                .component {
                    background: #fef2f2;
                    border: 1px solid #fecaca;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 10px 0;
                }
                .component-name {
                    font-weight: bold;
                    color: #dc2626;
                    margin-bottom: 8px;
                }
                .component-description {
                    color: #374151;
                    line-height: 1.5;
                }
                .footer {
                    text-align: center;
                    margin-top: 40px;
                    padding: 30px 20px;
                    color: #6b7280;
                    font-size: 0.9em;
                    border-top: 1px solid #e5e7eb;
                }

                .footer-content {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 16px;
                }

                .aicoe-logo {
                    background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    display: inline-flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 2px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                .logo-text {
                    font-size: 16px;
                    font-weight: 700;
                    letter-spacing: 1px;
                }

                .logo-subtitle {
                    font-size: 11px;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    opacity: 0.9;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>System Architecture</h1>
            </div>

            <div class="section">
                <h2>Architecture Overview</h2>
                <p><xsl:value-of select="description"/></p>
            </div>

            <div class="section">
                <h2>Architecture Diagram</h2>
                <div class="diagram-container">
                    <div class="mermaid">
                        <xsl:value-of select="diagram"/>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Component Breakdown</h2>
                <xsl:for-each select="componentBreakdown/component">
                    <div class="component">
                        <div class="component-name"><xsl:value-of select="@name"/></div>
                        <div class="component-description"><xsl:value-of select="."/></div>
                    </div>
                </xsl:for-each>
            </div>

            <div class="footer">
                <div class="footer-content">
                    <div class="aicoe-logo">
                        <span class="logo-text">AICOE</span>
                        <span class="logo-subtitle">AI-Powered Solutions</span>
                    </div>
                    <p>Generated by AICOE Platform</p>
                </div>
            </div>

            <script>
                mermaid.initialize({ startOnLoad: true });
            </script>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>