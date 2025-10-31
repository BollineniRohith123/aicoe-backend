<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <!-- Main template -->
    <xsl:template match="/productRequirementsDocument">
        <html lang="en">
        <head>
            <meta charset="UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title><xsl:value-of select="title"/></title>
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
                    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
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
                    color: #1e3a8a;
                    border-bottom: 2px solid #3b82f6;
                    padding-bottom: 10px;
                    margin-top: 0;
                }
                .section h3 {
                    color: #374151;
                    margin-top: 20px;
                }
                .goal, .requirement {
                    background: #f3f4f6;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #3b82f6;
                    border-radius: 4px;
                }
                .use-case {
                    background: #f9fafb;
                    padding: 20px;
                    margin: 15px 0;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                }
                .use-case h4 {
                    color: #1e3a8a;
                    margin-top: 0;
                }
                .actor {
                    display: inline-block;
                    background: #dbeafe;
                    color: #1e3a8a;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 0.9em;
                    margin: 2px;
                }
                .flow-step {
                    margin: 5px 0;
                    padding-left: 20px;
                }
                .flow-step:before {
                    content: "•";
                    color: #3b82f6;
                    font-weight: bold;
                    margin-right: 10px;
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
                <h1><xsl:value-of select="title"/></h1>
            </div>

            <div class="section">
                <h2>Executive Summary</h2>
                <p><xsl:value-of select="executiveSummary"/></p>
            </div>

            <div class="section">
                <h2>Project Scope</h2>
                <div>
                    <h3>In Scope</h3>
                    <p><xsl:value-of select="scope/inScope"/></p>
                </div>
                <div>
                    <h3>Out of Scope</h3>
                    <p><xsl:value-of select="scope/outOfScope"/></p>
                </div>
            </div>

            <div class="section">
                <h2>Business Goals</h2>
                <xsl:for-each select="businessGoals/goal">
                    <div class="goal">
                        <xsl:value-of select="."/>
                    </div>
                </xsl:for-each>
            </div>

            <div class="section">
                <h2>Use Cases</h2>
                <xsl:for-each select="useCases/useCaseModel/useCase">
                    <div class="use-case">
                        <h4><xsl:value-of select="title"/></h4>
                        <p><strong>Primary Actor:</strong> <span class="actor"><xsl:value-of select="primaryActor"/></span></p>
                        <xsl:if test="secondaryActors/actor">
                            <p><strong>Secondary Actors:</strong>
                                <xsl:for-each select="secondaryActors/actor">
                                    <span class="actor"><xsl:value-of select="."/></span>
                                </xsl:for-each>
                            </p>
                        </xsl:if>
                        <p><strong>Description:</strong> <xsl:value-of select="description"/></p>

                        <h5>Main Flow</h5>
                        <div class="flow">
                            <xsl:for-each select="mainFlow/step">
                                <div class="flow-step"><xsl:value-of select="."/></div>
                            </xsl:for-each>
                        </div>

                        <xsl:if test="alternativeFlows/flow">
                            <h5>Alternative Flows</h5>
                            <xsl:for-each select="alternativeFlows/flow">
                                <div class="flow">
                                    <strong><xsl:value-of select="@id"/>: <xsl:value-of select="@trigger"/></strong>
                                    <xsl:for-each select="step">
                                        <div class="flow-step"><xsl:value-of select="."/></div>
                                    </xsl:for-each>
                                </div>
                            </xsl:for-each>
                        </xsl:if>

                        <xsl:if test="exceptionFlows/flow">
                            <h5>Exception Flows</h5>
                            <xsl:for-each select="exceptionFlows/flow">
                                <div class="flow">
                                    <strong><xsl:value-of select="@id"/>: <xsl:value-of select="@trigger"/></strong>
                                    <xsl:for-each select="step">
                                        <div class="flow-step"><xsl:value-of select="."/></div>
                                    </xsl:for-each>
                                </div>
                            </xsl:for-each>
                        </xsl:if>
                    </div>
                </xsl:for-each>
            </div>

            <div class="section">
                <h2>Non-Functional Requirements</h2>
                <xsl:for-each select="nonFunctionalRequirements/requirement">
                    <div class="requirement">
                        <strong><xsl:value-of select="@type"/>: </strong>
                        <xsl:value-of select="."/>
                    </div>
                </xsl:for-each>
            </div>

            <div class="footer">
                <p>Generated by AICOE Platform</p>
            </div>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>