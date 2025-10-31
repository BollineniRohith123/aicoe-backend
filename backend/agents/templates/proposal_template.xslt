<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <!-- Main template -->
    <xsl:template match="/commercialProposal">
        <html lang="en">
        <head>
            <meta charset="UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Commercial Proposal</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }
                .header {
                    background: linear-gradient(135deg, #059669, #10b981);
                    color: white;
                    padding: 40px;
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
                    padding: 30px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .section h2 {
                    color: #059669;
                    border-bottom: 2px solid #10b981;
                    padding-bottom: 10px;
                    margin-top: 0;
                }
                .section h3 {
                    color: #374151;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }
                .timeline-phase {
                    background: #f0fdf4;
                    border: 1px solid #bbf7d0;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 10px 0;
                }
                .phase-name {
                    font-weight: bold;
                    color: #059669;
                }
                .phase-duration {
                    color: #6b7280;
                    font-size: 0.9em;
                }
                .pricing-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                .pricing-table th, .pricing-table td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #e5e7eb;
                }
                .pricing-table th {
                    background: #f9fafb;
                    font-weight: 600;
                    color: #374151;
                }
                .pricing-item {
                    background: #f0fdf4;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 6px;
                    border-left: 4px solid #10b981;
                }
                .currency {
                    font-weight: bold;
                    color: #059669;
                }
                .highlight {
                    background: #fef3c7;
                    padding: 15px;
                    border-radius: 6px;
                    border-left: 4px solid #f59e0b;
                    margin: 20px 0;
                }
                .footer {
                    text-align: center;
                    margin-top: 40px;
                    padding: 20px;
                    color: #6b7280;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Commercial Proposal</h1>
            </div>

            <div class="section">
                <h2>Introduction</h2>
                <p><xsl:value-of select="introduction"/></p>
            </div>

            <div class="section">
                <h2>Scope of Work</h2>
                <p><xsl:value-of select="scopeOfWork"/></p>
            </div>

            <div class="section">
                <h2>Project Timeline</h2>
                <xsl:for-each select="timeline/phase">
                    <div class="timeline-phase">
                        <div class="phase-name"><xsl:value-of select="@name"/></div>
                        <div class="phase-duration">Duration: <xsl:value-of select="@durationWeeks"/> weeks</div>
                    </div>
                </xsl:for-each>
            </div>

            <div class="section">
                <h2>Pricing</h2>

                <h3>Services</h3>
                <table class="pricing-table">
                    <thead>
                        <tr>
                            <th>Service</th>
                            <th>Rate</th>
                            <th>Unit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="pricing/services/item">
                            <tr>
                                <td><xsl:value-of select="@name"/></td>
                                <td class="currency"><xsl:value-of select="@rate"/> <xsl:value-of select="@currency"/></td>
                                <td><xsl:value-of select="@unit"/></td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>

                <h3>Infrastructure Costs</h3>
                <div class="highlight">
                    <strong>Estimated Monthly Cloud Costs:</strong>
                    <span class="currency"><xsl:value-of select="pricing/infrastructure/item/@rate"/> <xsl:value-of select="pricing/infrastructure/item/@currency"/></span>
                    <xsl:value-of select="pricing/infrastructure/item/@unit"/>
                    <br/>
                    <small><em><xsl:value-of select="pricing/infrastructure/item/@notes"/></em></small>
                </div>
            </div>

            <div class="section">
                <h2>Next Steps</h2>
                <p><xsl:value-of select="nextSteps"/></p>
            </div>

            <div class="footer">
                <p>Generated by AICOE Platform</p>
            </div>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>