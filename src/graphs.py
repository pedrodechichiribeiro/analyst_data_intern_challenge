# This is the file that handles all specific SQL commands and graph configuration.

import matplotlib.pyplot as plt
import pandas as pd

class GraphLibrary:
    def __init__(self, db_manager):
        self.db = db_manager
        
    # Below we generate multiple graphs that i believe have value when doing a data analysis.
    
    # 1 - TOP 10 PRODUCTS GRAPH
    
    def plot_top_products(self, ax):
        
        sql = """ SELECT case_product, COUNT(*) as count
            FROM cases
            GROUP BY case_product
            ORDER BY count DESC
            LIMIT 10
        """
        df = self.db.get_query(sql) # uses a function from data_manager.py to get the results of the query
        
        # Plotting the graph
        
        ax.barh(df['case_product'], df['count'], color='#3498db')
        ax.invert_yaxis() # makes the most popular products the top ones
        ax.set_title('Top Products by Ticket Number')
        ax.set_xlabel('Number of Cases')
        
        # 1.1 - AI SPECIFIC CONTEXT
        
        # As a demonstration this program utilizes an quantized AI model to generate on-the-go analytics from the data.
        # For better and more useful results each graph, chart or general math results will have it's own contextual prompt
        # This allow for a better fine tuning of the response, something needed on lighter LLMs who tend to hallucinate more easily
        
        top_product = df.iloc[0]['case_product']
        top_count = df.iloc[0]['count']
        total_volume = df['count'].sum()
        share = (top_count / total_volume) * 100
        
        data_context = (
            f"The top product '{top_product}' has {top_count} cases, representing {share:.1f}% of the top 10 volume. "
            f"The 10th product only has {df.iloc[-1]['count']} cases."
        )
        
        system_prompt = (
            "You are a Product Manager. "
            "If one product represents over 30% of cases, declare it a 'Critical Stability Risk'. "
            "Otherwise, describe the distribution as 'Balanced'."
        )
        
        return system_prompt, data_context
        
    # 2 - SEVERITY BY PRODUCT (Stacked)
        
    def plot_severity_stack(self, ax):
        """
        Renders a grouped bar chart for better legibility of low-volume/high-severity cases.
        """
        # 1. Fetch Top 5 Products
        top_prod_sql = "SELECT case_product FROM cases GROUP BY case_product ORDER BY COUNT(*) DESC LIMIT 10"
        top_prods = self.db.get_query(top_prod_sql)['case_product'].tolist()
        
        # 2. Query data for these products
        sql = f"SELECT case_product, case_severity, COUNT(*) as count FROM cases WHERE case_product IN ({str(top_prods)[1:-1]}) GROUP BY case_product, case_severity"
        df = self.db.get_query(sql)
        
        # Pivot and Normalize to Percentages
        pivot_df = df.pivot(index='case_product', columns='case_severity', values='count').fillna(0)
        pivot_perc = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100
        
        # Define strict order and color scheme
        severity_colors = {'Low': '#2ecc71', 'Normal': '#f1c40f', 'Medium': '#e67e22', 'High': '#e74c3c', 'Urgent': '#8b0000'}
        desired_order = [s for s in ['Low', 'Normal', 'Medium', 'High', 'Urgent'] if s in pivot_perc.columns]
        pivot_perc = pivot_perc[desired_order]

        # IMPROVEMENT: Use Grouped Bar instead of Stacked for clarity
        pivot_perc.plot(kind='barh', ax=ax, color=[severity_colors[s] for s in desired_order], width=0.8)

        # Better Labeling: Place text at the end of bars rather than inside
        for p in ax.patches:
            width = p.get_width()
            if width > 0: # Only label non-zero values
                ax.text(width + 1, p.get_y() + p.get_height()/2, f'{width:.1f}%', 
                        va='center', fontsize=8, fontweight='bold')

        ax.set_title('Product Risk Profile: Severity Distribution', pad=20)
        ax.set_xlabel('Percentage of Tickets (%)')
        ax.set_ylabel('')
        ax.set_xlim(0, 115) # Extra space for the labels
        ax.legend(title='Severity', loc='lower right', fontsize='small')
        
        # AI Context Update
        worst_prod = pivot_perc['Urgent'].idxmax() if 'Urgent' in pivot_perc else "N/A"
        data_context = f"Analysis of top 10 products. Product with highest urgent ratio: {worst_prod}."
        system_prompt = "You are a Risk Auditor. Identify which product has the most volatile severity distribution."

        return system_prompt, data_context
    
    # 3 - CASE TYPES (Grouped "Other")

    def plot_case_types(self, ax):
        sql = "SELECT case_type, COUNT(*) as count FROM cases GROUP BY case_type ORDER BY count DESC"
        df = self.db.get_query(sql)
        
        # Group small slices
        total_cases = df['count'].sum()
        threshold = 0.03 
        
        mask = (df['count'] / total_cases) >= threshold
        df_big = df[mask].copy()
        small_sum = df[~mask]['count'].sum()
        
        if small_sum > 0:
            new_row = pd.DataFrame([{'case_type': 'Other', 'count': small_sum}])
            df_final = pd.concat([df_big, new_row], ignore_index=True)
        else:
            df_final = df_big
        
        # Plotting
        
        ax.pie(
            df_final['count'],
            labels=df_final['case_type'],
            autopct='%1.1f%%',
            startangle=90,
            radius=0.85,
            wedgeprops=dict(width=0.3)
        )
        ax.set_title('Distribution of Case Types')
        
        # 3.1 - AI CONTEXT 
        
        # We fetch the top 3 specific types so the AI doesn't have to guess
        
        top_3 = df.head(3)
        context_list = []
        for index, row in top_3.iterrows():
            pct = (row['count'] / total_cases) * 100
            context_list.append(f"{row['case_type']} ({pct:.1f}%)")
            
        data_str = ", ".join(context_list)
        
        data_context = f"Total Cases analyzed: {total_cases}. The top 3 categories are: {data_str}."
        
        system_prompt = (
            "You are a Support Team Lead. "
            "Look at the top 3 categories provided. "
            "If 'Bug' or 'Defect' is in the top 3, recommend 'Engineering Review'. "
            "If 'Question' or 'Training' is dominant, recommend 'Update Knowledge Base'. "
        )    
        
        return system_prompt, data_context
    
    # 4 - GLOBAL HEAT MAP (Countries by case volume)
    
    def plot_global_hotspots(self, ax):
        
        sql = """
            SELECT a.account_country, COUNT(c.case_sfid) as count
            FROM cases c
            JOIN accounts a ON c.account_sfid = a.account_sfid
            GROUP BY a.account_country
            ORDER BY count DESC
            LIMIT 10
        """
        df = self.db.get_query(sql)
        
        # Plotting
        
        ax.bar(df['account_country'], df['count'], color="#ab6ec4")
        ax.set_title('Top 10 Countries by Support Load')
        ax.set_ylabel('Total Cases')
        ax.tick_params(axis='x', rotation=45)
        
        # 4.1 - AI CONTEXT (takes into account Canadian bias)
        
        # Some tests showed that the AI tends to interpret the high ticket density from Canada as problematic
        # That's not necessarily a problem, since it's mostly due to the company being from Canada, so
        # It's normal for a increased ticket count and density on that region.
        
        if not df.empty:
            top_country = df.iloc[0]['account_country']
            top_count = df.iloc[0]['count']
            total_cases = df['count'].sum()
            
            # check rank of Canada
            can_row = df[df['account_country'] == 'Canada']
            can_vol = can_row.iloc[0]['count'] if not can_row.empty else 0
            
            data_context = (
                f"Global Vision HQ Location: Canada. "
                f"Top Country: {top_country} ({top_count} cases). "
                f"Canada Volume: {can_vol} cases. "
                f"The top country represents {(top_count/total_cases)*100:.1f}% of the top 10 volume."
            )
        else:
            data_context = "No country data available."
        
        system_prompt = (
            "You are a Regional Operations Director for GlobalVision (a Canadian company). "
            "Expect Canada to have the highest volume (Domestic Market). Do not flag high Canadian volume as an error. "
            "Instead, focus on the #2 and #3 countries. Are they growing disproportionately? "
            "Identify if we need language support for the biggest non-Canadian region."
        )
        
        return system_prompt, data_context
    
    # 5 - TICKET DENSITY ANALYSIS
    
    def plot_ticket_density(self, ax):

        sql = """
            WITH CaseCounts AS (
                SELECT 
                    a.account_country, 
                    COUNT(c.case_sfid) as total_cases
                FROM accounts a
                LEFT JOIN cases c ON a.account_sfid = c.account_sfid
                GROUP BY a.account_country
            ),
            AccountCounts AS (
                SELECT 
                    account_country, 
                    COUNT(DISTINCT account_sfid) as total_customers
                FROM accounts
                GROUP BY account_country
            )
            SELECT 
                ac.account_country,
                (CAST(cc.total_cases AS FLOAT) / ac.total_customers) as density
            FROM AccountCounts ac
            JOIN CaseCounts cc ON ac.account_country = cc.account_country
            WHERE ac.total_customers > 5  
            ORDER BY density DESC
            LIMIT 10
        """
        
        df = self.db.get_query(sql)
        
        # Plotting
        ax.barh(df['account_country'], df['density'], color='#d35400') 
        ax.invert_yaxis()
        ax.set_title('Support Density (Tickets per Account)')
        ax.set_xlabel('Avg Tickets per Customer')

        # 5.1 - AI CONTEXT (same as the heat map, adjusted for Canadian bias)
        
        if not df.empty:
            top_country = df.iloc[0]['account_country']
            top_val = df.iloc[0]['density']
            
            # Get Canada density for comparison
            can_row = df[df['account_country'] == 'Canada']
            can_density = can_row.iloc[0]['density'] if not can_row.empty else 0.0
            
            data_context = (
                f"Global Vision is a Canadian Company. "
                f"Top Density Region: {top_country} ({top_val:.2f} tickets/user). "
                f"Home Market (Canada) Density: {can_density:.2f} tickets/user. "
                f"Global Average Density: {df['density'].mean():.2f}."
            )
        else:
            data_context = "No density data available."
        
        system_prompt = (
            "You are a CX Analyst. Analyze the 'Neediness' of regions. "
            "Treat Canada as the baseline (Standard behavior). "
            "If a region has significantly HIGHER density than Canada, flag it as a 'Problem Area' (Training/Bugs). "
            "If a region has much LOWER density, flag it as 'Low Engagement' or 'Silent Churn Risk'."
        )
        
        return system_prompt, data_context
    
    # 6 - INDUSTRY STRUGGLES
    
    def plot_industry_struggles(self, ax):
        sql = """
            SELECT a.account_industry, COUNT(c.case_sfid) as count 
            FROM cases c
            JOIN accounts a ON c.account_sfid = a.account_sfid
            GROUP BY a.account_industry
            ORDER BY count DESC
            LIMIT 10
        """
        df = self.db.get_query(sql)
        
        # Plotting
        ax.barh(df['account_industry'], df['count'], color='#16a085') 
        ax.invert_yaxis()
        ax.set_title('Total Cases by Client Industry')
        ax.set_xlabel('Number of Cases')

        # 6.1 - AI CONTEXT 
        
        # Had some problems regarding math conclusions, so heavier Python math was implemented
        # Instead of leaving the analysis to Gemma
        
        if not df.empty:
            top_ind = df.iloc[0]['account_industry']
            top_count = df.iloc[0]['count']
            total_cases = df['count'].sum()
            
            # Calculate Share
            share_pct = (top_count / total_cases) * 100
            
            risk_threshold = 40.0
            is_risk = share_pct > risk_threshold
            
            status_str = "CRITICAL RISK" if is_risk else "SAFE / DIVERSIFIED"
            comparison_str = "HIGHER" if is_risk else "LOWER"
            
            data_context = (
                f"Top Industry: '{top_ind}' ({share_pct:.1f}% of volume). "
                f"Risk Threshold: {risk_threshold}%. "
                f"Current Status: {status_str} (The value {share_pct:.1f}% is {comparison_str} than {risk_threshold}%)."
            )
        else:
            data_context = "No industry data available."
        
        system_prompt = (
            "You are a Product Strategist. Analyze the provided status. "
            "If status is 'CRITICAL RISK', warn about over-dependency on one sector. "
            "If status is 'SAFE', commend the healthy diversification. "
            "Do not perform your own math comparison; trust the Status provided."
        )
        
        return system_prompt, data_context
    
    # 7 - VOLUME OVER TIME (Weekly)
    
    def plot_volume_over_time(self, ax):
        sql = """
            SELECT strftime('%Y-%m-%d', case_created_date) as date, COUNT(*) as count
            FROM cases
            GROUP BY date
            ORDER BY date ASC
        """
        
        df = self.db.get_query(sql)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        # Resample to weekly to smooth out noise
        df_weekly = df.resample('W').sum().reset_index()
        
        # Plotting
        ax.plot(df_weekly['date'], df_weekly['count'], marker='o', linestyle='-', color="#4291c5")
        ax.set_title('Weekly Ticket Volume Trend')
        ax.set_ylabel('New Cases (Weekly)')
        ax.grid(True)
        
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        
        # 7.1 - AI CONTEXT 
        
        if len(df_weekly) >= 2:
            # Compare first 4 weeks average vs last 4 weeks average to perceive any ongoing trends
            start_avg = df_weekly.head(4)['count'].mean()
            end_avg = df_weekly.tail(4)['count'].mean()
            
            # Protect against division by zero
            if start_avg > 0:
                growth_pct = ((end_avg - start_avg) / start_avg) * 100
            else:
                growth_pct = 100 if end_avg > 0 else 0
            
            trend_desc = "Surging" if growth_pct > 20 else "Stable" if abs(growth_pct) < 10 else "Dropping"
            
            data_context = (
                f"Trend Analysis ({len(df_weekly)} weeks observed): "
                f"Start Average: {start_avg:.1f} cases/week. "
                f"Recent Average: {end_avg:.1f} cases/week. "
                f"Net Change: {growth_pct:+.1f}%. "
                f"Classification: {trend_desc}."
            )
        else:
            data_context = "Insufficient time data to determine trend."
        
        system_prompt = (
            "You are a Staffing Planner. "
            "Use the 'Net Change' percentage to decide. "
            "If change is > +15%, recommend 'Immediate Hiring'. "
            "If change is between -10% and +10%, recommend 'Maintain Staff'. "
            "If change is < -15%, recommend 'Review Efficiency'."
        )
        
        return system_prompt, data_context
    
    # 8 - TIME TO RESOLUTION (histogram)
    
    def plot_resolution_time(self, ax):
        sql = """
            SELECT (julianday(case_closed_date) - julianday(case_created_date)) as days
            FROM cases
            WHERE case_status = 'Closed' AND case_closed_date IS NOT NULL
        """
        
        df = self.db.get_query(sql)
        
        # Plotting
        
        ax.hist(df['days'], bins=40, color="#9949bb", edgecolor='white', alpha=0.7)
        ax.set_title('Time to Resolution Distribution')
        ax.set_xlabel('Days to Close')
        ax.set_ylabel('Number of Cases')
        
        # Dynamically set the limit instead of hardcoding 100
        # Adding a 10% buffer to the max value so the bar doesn't touch the edge
        
        if not df.empty:
            avg_days = df['days'].mean()
            median_days = df['days'].median()
            max_days = df['days'].max()
            std_dev = df['days'].std()
            
            data_context = (
                f"Average Resolution: {avg_days:.1f} days. "
                f"Median Resolution: {median_days:.1f} days. "
                f"Worst Outlier: {max_days:.1f} days. "
                f"Standard Deviation: {std_dev:.1f}."
            )
        else:
            data_context = "No closed cases."

        system_prompt = (
            "You are an Operations Manager. "
            "Compare the Mean vs Median. If Mean is much higher, we have a 'Long Tail' problem (old tickets stuck). "
            "If they are close, the process is consistent."
        )
        
        return system_prompt, data_context
    
    # 9 - BACKLOG GROWTH (unfinished tasks)
    
    def plot_backlog_growth(self, ax):
        
        #date of creation
        df_created = self.db.get_query("SELECT strftime('%Y-%m-%d', case_created_date) as date, COUNT(*) as val FROM cases GROUP BY date")
        # date of closure
        df_closed = self.db.get_query("SELECT strftime('%Y-%m-%d', case_closed_date) as date, COUNT(*) as val FROM cases WHERE case_closed_date IS NOT NULL GROUP BY date")
        
        df_created['date'] = pd.to_datetime(df_created['date'])
        df_closed['date'] = pd.to_datetime(df_closed['date'])
        
        merged = pd.merge(df_created, df_closed, on='date', how='outer', suffixes=('_new','_resolved')).fillna(0)
        merged = merged.sort_values('date')
        
        merged['total_created'] = merged['val_new'].cumsum()
        merged['total_closed'] = merged['val_resolved'].cumsum()
        
        ax.plot(merged['date'], merged['total_created'], color='red', label='Total Received')
        ax.plot(merged['date'], merged['total_closed'], color='green', label='Total Resolved')
        
        ax.fill_between(merged['date'], merged['total_created'], merged['total_closed'], color='gray', alpha=0.1)
        
        ax.set_title('Backlog Growth (Received vs Resolved)')
        ax.legend()
        ax.grid(True)
        ax.figure.autofmt_xdate()
        
        # 9.1 - AI CONTEXT
        
        current_backlog = merged.iloc[-1]['total_created'] - merged.iloc[-1]['total_closed']
        start_backlog = merged.iloc[0]['total_created'] - merged.iloc[0]['total_closed']
        growth = current_backlog - start_backlog
        
        data_context = (
            f"Backlog started at {start_backlog} and is now {current_backlog}. "
            f"Net change: {'+' if growth > 0 else ''}{growth} cases pending."
        )
        
        system_prompt = (
            "You are a Resource Planner. "
            "Analyze the net change in backlog. "
            "If positive, estimate how many extra agents are needed (assuming 1 agent handles 5 tickets/day)."
        )
        
        return system_prompt, data_context#