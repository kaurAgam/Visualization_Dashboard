from django.shortcuts import render
from .models import Insight
from django.core.paginator import Paginator

from django.http import JsonResponse
import plotly.express as px

def dashboard(request):
    insights=Insight.objects.all()

        
    # chart starts

    fig = px.density_heatmap(
        x=[c.likelihood for c in insights],
        y=[c.relevance for c in insights],
        title='Density Histogram of Likelihood and Relevance'
    )
    fig.update_layout(height=400, width=530,xaxis_title='Likelihood',yaxis_title='Relevance')
    chart=fig.to_html()

    fig2 = px.bar(
        x=[c.intensity for c in insights],
        y=[c.sector for c in insights], 
        title="Intensity for different sectors")
    fig2.update_layout(height=400, width=530,xaxis_title='Intensity',yaxis_title='Sector')
    chart2=fig2.to_html()

    fig3 = px.density_contour(
        x=[c.pestle for c in insights],
        y=[c.impact for c in insights], 
        title="Impact by PESTLE")
    fig3.update_layout(height=400, width=530,xaxis_title='PESTLE',yaxis_title='IMPACT')
    chart3=fig3.to_html()

    fig4 = px.histogram(
        x=[c.topic for c in insights],
        title="Topics")
    fig4.update_layout(height=400, width=530,xaxis_title='Country',yaxis_title='Count')
    chart4=fig4.to_html()
    # chart ends





    searched_for=''

    if request.GET.get('search_input'):
        searched_for=request.GET.get('search_input')
        insights= (insights.filter(title__icontains=request.GET.get('search_input'))  | insights.filter(sector__icontains=request.GET.get('search_input')) | insights.filter(topic__icontains=request.GET.get('search_input'))).distinct() 


    pestle_opts = sorted(Insight.objects.values_list('pestle', flat=True).distinct())
    topic_opts = sorted(Insight.objects.values_list('topic', flat=True).distinct())
    sector_opts = sorted(Insight.objects.values_list('sector', flat=True).distinct())
    region_opts = sorted(Insight.objects.values_list('region', flat=True).distinct())
    country_opts = sorted(Insight.objects.values_list('country', flat=True).distinct())

    selected_pestle = request.GET.get('pestle')
    selected_topic = request.GET.get('topic')
    selected_sector = request.GET.get('sector')
    selected_region = request.GET.get('region')
    selected_country = request.GET.get('country')
    
    sort_by = request.GET.get('sort_by', 'relevance')  # Default to sorting by relevance
    sort_order = request.GET.get('sort_order', 'desc')  # Default to descending order

    

    if request.GET.get('reset'):
        selected_pestle = None
        selected_topic = None
        selected_sector = None
        selected_region = None
        selected_country = None
        sort_by = 'relevance'
        sort_order = 'desc'
        searched_for=''
        insights=Insight.objects.all()

    if selected_pestle:
        insights = insights.filter(pestle=selected_pestle)
    if selected_topic:
        insights = insights.filter(topic__icontains=selected_topic)
    if selected_sector:
        insights = insights.filter(sector__icontains=selected_sector)
    if selected_region:
        insights = insights.filter(region__icontains=selected_region)
    if selected_country:
        insights = insights.filter(country__icontains=selected_country)

    
    if sort_by == 'relevance':
        insights = insights.order_by(f'-relevance' if sort_order == 'desc' else 'relevance', '-likelihood')
    elif sort_by == 'likelihood':
        insights = insights.order_by(f'-likelihood' if sort_order == 'desc' else 'likelihood', '-relevance')





    items_per_page =5
    paginator=Paginator(insights,items_per_page)
    page_number=request.GET.get('page')
    page_obj =paginator.get_page(page_number)

    return render(request,'home/dashboard.html',{'page_obj':page_obj,
                                                 'searched_for':searched_for,
                                                 'pestle_opts': pestle_opts,
                                                 'topic_opts': topic_opts,
                                                 'sector_opts': sector_opts,
                                                 'region_opts': region_opts,
                                                 'country_opts': country_opts,
                                                 'selected_pestle': selected_pestle,
                                                 'selected_topic': selected_topic,
                                                 'selected_sector': selected_sector,
                                                 'selected_region': selected_region,
                                                 'selected_country': selected_country,
                                                 'sort_by': sort_by,
                                                 'sort_order': sort_order,
                                                 'chart':chart,
                                                 'chart2':chart2,
                                                 'chart3':chart3,
                                                 'chart4':chart4,
                                                 })