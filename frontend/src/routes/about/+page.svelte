<script lang="ts">
    // This line receives the `data` object from your +page.ts's `load` function.
    // The erroneous lines trying to set `$page.title` have been removed.
    export let data;
</script>

<!-- This svelte:head block correctly uses the data from the load function -->
<svelte:head>
    <title>{data.title}</title>
    <meta name="description" content={data.description} />
</svelte:head>

<div class="page-container">
    <div class="glass card">
        <div class="card-header">
            <h1>About TerraPulse</h1>
            <p class="subtitle">Planetary Health Monitoring & Prediction</p>
        </div>
        
        <div class="card-content">
            <p>
                TerraPulse is an advanced AI-powered platform designed to monitor planetary health in real-time
                and predict environmental anomalies before they become crises. Our mission is to provide actionable
                intelligence for a more resilient and sustainable future.
            </p>
            
            <h2>Our Technology</h2>
            <p>
                Using cutting-edge machine learning models and satellite data from NASA, ESA, and other sources,
                TerraPulse goes beyond simple data visualization to provide predictive insights about environmental
                events like wildfires, floods, storms, and more.
            </p>
            
            <div class="features-grid">
                <div class="feature">
                    <div class="feature-icon">🛰️</div>
                    <h3>Real-Time Satellite Data</h3>
                    <p>Access to multiple satellite data sources for comprehensive coverage</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🧠</div>
                    <h3>AI-Powered Predictions</h3>
                    <p>Machine learning models predict environmental events before they escalate</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🌍</div>
                    <h3>Global Coverage</h3>
                    <p>Monitor the entire planet with detailed regional insights</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🔔</div>
                    <h3>Real-Time Alerts</h3>
                    <p>Instant notifications about critical environmental events</p>
                </div>
            </div>
            
            <h2>Our Mission</h2>
            <p>
                At TerraPulse, we believe that advanced technology should be harnessed to protect our planet
                and its inhabitants. By providing early warnings and predictive insights, we aim to:
            </p>
            
            <ul>
                <li>Save lives through early disaster warnings</li>
                <li>Reduce environmental damage through proactive measures</li>
                <li>Support scientific research with comprehensive data</li>
                <li>Empower communities with accessible environmental intelligence</li>
            </ul>
        </div>
    </div>
</div>

<style>
    .page-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .feature {
        text-align: center;
        padding: 20px;
        background: rgba(0, 0, 0, 0.2);
        /* Make sure you have this CSS variable defined in a global stylesheet */
        border-radius: var(--border-radius, 8px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature h3 {
        margin-bottom: 10px;
        color: var(--accent-primary);
    }
    
    ul {
        padding-left: 20px;
        margin: 15px 0;
    }
    
    li {
        margin-bottom: 8px;
    }
</style>
