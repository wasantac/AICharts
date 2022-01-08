import sys
sys.path.append('./chartslib')

import xNB_Clasification,AICharts_Report
know = xNB_Clasification.learning_process('crude',xNB_Clasification.pre_procesing_train('./processed/reuters-training.dat'),xNB_Clasification.pre_processing_cat('./processed/reuters-cat-doc.qrels'))
test1 = '''The issue price of the European
Investment Bank 300 mln guilder 6.25 pct bullet bond due
1995, announced on April 1, has been set at par, lead manager
Amro bank said.
    Subscriptions remain open until 1300 gmt tomorrow, April 9.
    Payment is due May 14 and coupon date is May 15.'''
tokenized = xNB_Clasification.transform(test1)
ev = xNB_Clasification.evaluation_process(tokenized,know)
print(ev)
print(ev.buoyancy())
final_data = xNB_Clasification.set_weights(test1,ev)
final_data = xNB_Clasification.set_weights(test1,ev,weight_value=10)
text_list = final_data[0].split(" ")
AICharts_Report.AIChart_plot_data_word_graph(final_data[1],text_list=text_list,title="Grain",saveImg=True)