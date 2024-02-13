import concurrent.futures #import used to parallelise analysis
import argparse
import ast
import glob
import csv
import numpy as np
import subprocess
import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from datetime import date
from scipy import stats
import sys
sys.path.append("/data/jfuller")
sys.path.append("/data/jfuller/AnalysisTools/")
import AnalysisTools.CharacterisationTools as analysis
import AnalysisTools.Algos as algo
import  AnalysisTools.IVAnalysis as IVAnalysis
import csv
from scipy import interpolate


###########
#Functions
###########
def process_channel_data(x,pkp,pkt,charge,chrms,channel,channelrms):
    TriggerPos,std,trig_err = pa.GetTriggerPosition(pkt[(pkt>-9999) & (channel == x)].flatten(),nBins=500, method="max")
    Trig_left = TriggerPos - pa.PromptRoiLeft*pa.SamplingRate
    Trig_right = TriggerPos + pa.PromptRoiRight*pa.SamplingRate 
    Trigger_ROI_left = Trig_left   #sample number
    Trigger_ROI_right = Trig_right #sample number
    pkp_trig = pkp[(pkt>Trigger_ROI_left) & (pkt<Trigger_ROI_right) & (channel == x)]
    pkt_trig = pkt[(pkt>Trigger_ROI_left) & (pkt<Trigger_ROI_right) & (channel == x)]
    charge_trig = charge[(pkt>Trigger_ROI_left) & (pkt<Trigger_ROI_right) & (channel == x)]
 


    if plot == "True":
        plt.figure()
        plt.hist(charge[(charge>-9999) & (channel == x)].flatten(),bins=500,histtype="step",color = "m")#,range = [0,0.0035])
        plt.title("Channel {} Charge of Pulse".format(x))
        plt.xlabel("Charge [arb.]")
        plt.ylabel("count[#]")

        plt.figure()
        plt.hist(ADCmVConv*chrms[(chrms>-9999) & (channelrms == x)].flatten(),bins=200,histtype="step",color = "m", label= "RMS Mean: {}mV".format(ADCmVConv*np.mean(chrms[channelrms == x].flatten())))#,range = [ADCmVConv*0,ADCmVConv*400])
        plt.title("Channel {} RMS Distribution".format(x))
        plt.xlabel("RMS [mV]")
        plt.ylabel("count[#]")
        plt.legend()
        

        plt.figure()
        plt.hist(pkt[(pkt>-9999) & (channel == x)].flatten()/pa.SamplingRate*1e6,bins=250,histtype="step",color = "m")
        plt.title("Channel {} Time of Hits".format(x))
        plt.xlabel("Time [\u03BCs]")
        plt.ylabel("count[#]")
        plt.yscale("log")
        plt.axvline(Trig_right/pa.SamplingRate*1e6, color="k")
        plt.axvline(Trig_left/pa.SamplingRate*1e6, color="k")


        plt.figure()
        plt.hist(ADCmVConv*pkp[(pkp>-9999) & (channel == x)].flatten(),bins=500,histtype="step",color = "m")#,range=[ADCmVConv*0,ADCmVConv*5000])
        plt.title("Channel {} Amplitude of Hits".format(x))
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("count[#]")


        plt.figure()
        plt.hist(ADCmVConv*pkp_trig.flatten(),bins=500,histtype="step",color = "m")#,range=[0,100])
        plt.title("Channel {} Amplitude of Hits in trigger ROI".format(x))
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("count[#]")
        #plt.yscale("log")
        plt.show()

    elif plot == "False":
        pass


    ############################################
    #1PE and 2PE amplitude and charge extraction
    ############################################

    Amp1peMean, Amp1peStd, Amp1peError,Amp1peStdError,chi2,ndof = pa.Get1pePeak(pkp_trig.flatten(),
                                                                        bins = 500,
                                                                        PedestalThreshold =0,
                                                                        histRange =[0,4000],
                                                                        verbose=False,
                                                                        Plot=ast.literal_eval(plot),
                                                                        upper_threshold=750 ) 
    pe_threshold_upperLimit = Amp1peMean + 2*Amp1peStd
    pe_thresh_lowerLimit    = Amp1peMean - 2*Amp1peStd



    Amp2peMean, Amp2peStd, Amp2peError,Amp2peStdError,chi2_2,ndof_2 = pa.Get1pePeak(pkp_trig.flatten(),
                                                                        bins = 500,
                                                                        PedestalThreshold = pe_threshold_upperLimit,
                                                                        histRange =[0,4000],
                                                                        verbose=False,
                                                                        Plot=ast.literal_eval(plot),
                                                                        upper_threshold=None ) 
    TwoPE_threshold_upperLimit = Amp2peMean + 2*Amp1peStd
    TwoPE_thresh_lowerLimit    = Amp2peMean - 2*Amp1peStd


    Charge1peMean, Charge1peStd, Charge1peError,Charge1peStdError,chi2,ndof = pa.Get1pePeak(charge_trig.flatten(),
                                                                        bins = 500,
                                                                        PedestalThreshold = 0 ,
                                                                        histRange = [0,0.0035],
                                                                        verbose=False,
                                                                        Plot=ast.literal_eval(plot),
                                                                        upper_threshold=None) 
    pe_chargethreshold_upperLimit = Charge1peMean + 2*Charge1peStd
    pe_chargethresh_lowerLimit    = Charge1peMean - 2*Charge1peStd


    ########
    #SNR
    ########


    rms = np.mean(chrms[(channelrms==x) & (chrms>-9999)].flatten())
    SNR = (Amp2peMean-Amp1peMean)/rms
    SNRerr = algo.ErrorDivide((Amp2peMean-Amp1peMean),rms,algo.ErrorAddition(Amp1peError,Amp2peError),np.std(chrms[(channelrms==x) & (chrms>-9999)].flatten())/len(chrms[(channelrms==x) & (chrms>-9999)].flatten()))
    print("RMS (mV): {} +/- {}".format(rms*ADCmVConv,ADCmVConv*np.std(chrms[(channelrms==x) & (chrms>-9999)].flatten())/len(chrms[(channelrms==x) & (chrms>-9999)].flatten())))
    print("1PE Amplitude (mV): {} +/- {}".format(Amp1peMean*ADCmVConv,Amp1peError*ADCmVConv))
    print("2PE Amplitude (mV): {} +/- {}".format(Amp2peMean*ADCmVConv,Amp2peError*ADCmVConv))
    print("1PE Charge (.arb units): {} +/- {}".format(Charge1peMean,Charge1peError))
    print("Signal-to-Noise Ratio:{} +/- {}".format(SNR,SNRerr))


    #####
    #DCR
    #####

    pa.update_analysis_params(DarkNoiseRoiStart=3.2e-6)
    DN_rate_in_roi, DN_std, DN_rate_err= pa.GetDCR(pkt,pkp,pe_thresh_lowerLimit,
                                        pe_threshold_upperLimit,Plot=ast.literal_eval(plot),nbins=200,pk_ch=channel,channel_number=x)

    #print("Average Darknoise in the ROI: ", DN_rate_in_roi) 
    #print("DN Hz:", DN_rate_in_roi*us_to_Hz_normalisation)
    print("DN (Hz/mm^2)", ((DN_rate_in_roi*us_to_Hz_normalisation)/Tile_Area))
    #plt.show()

    #######
    #CDA
    ######
    CDA_Mean, CDA_std, CDA_mean_Err = pa.GetCDA(pkt,pkp,pe_threshold_upperLimit,pe_thresh_lowerLimit,200, Plot=ast.literal_eval(plot),pk_ch=channel,channel_number=x)
    DarknoiseSubtractedCDA = CDA_Mean - DN_rate_in_roi
    print("Mean CDA in ROI: ", CDA_Mean)
    print("Dark noise subtraced CDA: ", DarknoiseSubtractedCDA)

    #######
    #AP & DiCT
    #######
    N_APA, pkp_normStdError_0_5pe = pa.GetMeanAPA(pkp,pkt,Amp1peMean,Amp1peStd,pk_ch=channel,channel_number=x)
    DiCTProb = pa.GetDiCT(pkp,pkt,Amp1peMean,plot=ast.literal_eval(plot),nbins=250,pk_ch=channel,channel_number=x)
    print("Mean number of additional Prompt Avalanches: ", N_APA)
    print("Probability of DiCT: ",DiCTProb)
    return SNR,Amp1peMean,DN_rate_in_roi,CDA_Mean,rms,DiCTProb,SNRerr,Amp1peError,DN_rate_in_roi,CDA_std

##################
#Main Body
##################
if __name__ == '__main__':
    
   ################
    #Initialisation
    ################

    #Analysis Details default
    PromptRoiLeft = 0.3e-6 #seconds
    PromptRoiRight = 0.5e-6 #seconds
    CDAroiTime = 5e-6 #seconds
    DarkNoiseRoiTime = 9.6e-7 #seconds
    DN_start_from_trigger = -4e-06 #seconds
    Tile_Area = 2500 #mm^2
    SamplingRate = 125e6 #Samples/s
    ADCmVConv = 0.0305
    DN_start = 4e-06 #seconds
    us_to_Hz_normalisation = 1/DarkNoiseRoiTime #factor used to scale darknoise to Hz  

    # Input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-I","--InputReco",help ="Directory/to/data/for/spe")
    parser.add_argument("-P","--plot",help = "Plot = True or False")
    parser.add_argument("-B","--bias",help = "Bias voltage (V)")
    parser.add_argument("-T","--temp",help= "Warm(w) or Cold Test(c)")
    parser.add_argument("-C","--channel",help="q or t")
    args = parser.parse_args()
    
    #Assigning input arguments to variable
    plot = args.plot
    Bias = args.bias
    temp = args.temp
    chan = args.channel
    run_numbers_array = []
    spefilepath = args.InputReco

    
    #creating variabls for analysis quantaties
    pkt     = []
    pkp     = []
    charge  = []
    chrms   = []
    channel   = []

    BiasData = []
    SNRData = []
    ampData = []
    DNData =[]
    CDAData = []
    rmsData = []
    DiCTData = []

    SNR_Error = []
    amp_Error = []
    DN_Error  = []
    CDA_Error = []
    rms_Error = []
    DiCT_Error = []

    # Get the git version of the repositry this is to keep track of analysis done with different passport versions
    #today = date.today()
    #try:
    #    v = subprocess.check_output(['git', 'describe', '--tags','--abbrev=0'])
    #    GitVersion = str(v,'utf-8').strip() #Get tile passport Version
    #except: 
    #    print("Error reading Git tag")
    #    GitVersion = np.nan
    #datestr = today.strftime("%d_%m_%Y")

    
    #This needs to be cleaned up - essentially I give the user the option between testing single tiles mounted on the vPDU or to test full quadrants/channels.
    if args.InputReco:            
        pa = analysis.CharacterisationTools(PromptRoiLeft=PromptRoiLeft,PromptRoiRight=PromptRoiRight,PromptRoiTime=None,CDAroiTime = CDAroiTime,DarkNoiseRoiTime=DarkNoiseRoiTime, DarkNoiseRoiStart=DN_start,SamplingRate=SamplingRate)
        if chan == 't':
            while True:
                try:
                    num_tiles = int(input("Enter the number of tiles you want to test: "))
                    z = num_tiles
                    if num_tiles <= 0:
                        print("Please enter a positive integer greater than zero.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a positive integer greater than zero.")

            run_number = None
            while True:
                try:
                    run_number = int(input("Enter the starting run number: "))
                    if run_number < 0:
                        print("Please enter a non-negative integer.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a non-negative integer.")

            # Generate the array of run numbers
            #run_numbers_array = ['output{}.root'.format(run_number + i) for i in range(num_tiles)]
            run_number_array = "output01803.root"

        else:
            z = 4
            run_numbers_array = None
            pa.LoadFile(spefilepath)

            pkt     = pa.GetBranch("dstree","pk_t")   #Time of hits
            pkp     = pa.GetBranch("dstree","pk_p")   #Amplitude of each hit
            charge  = pa.GetBranch("dstree","pk_k")   #Integral of each hit
            chrms   = pa.GetBranch("dstree","ch_rms") #rms
            channel   = pa.GetBranch("dstree","pk_ch")  #Channel
            channelrms   = pa.GetBranch("dstree","ch_id")  #Channel

    else:
        pass


    ###########################
    #Channel Loop over SPE data
    ###########################

    
    if args.InputReco:
        if chan == 'q':
            for x in range(z):
                print("Processing channel {}".format(x))

                if len(pkt[(pkt>-9999) & (channel == x)].flatten())  < 100: 
                    continue
                
                SNR,Amp1peMean,DN_rate_in_roi,CDA_Mean,rms,DiCTProb,SNRerr,Amp1peError,DN_rate_in_roi,CDA_std = process_channel_data(x,pkp,pkt,charge,chrms,channel,channelrms)


                BiasData.append(Bias)
                SNRData.append(SNR)
                ampData.append(Amp1peMean*ADCmVConv)
                DNData.append((DN_rate_in_roi*us_to_Hz_normalisation)/(Tile_Area*4))
                CDAData.append(CDA_Mean)
                rmsData.append(rms*ADCmVConv)
                DiCTData.append(DiCTProb[0])

                #### Error Stuff ### 
                SNR_Error.append(SNRerr)
                amp_Error.append(Amp1peError*ADCmVConv)
                DN_Error.append((DN_rate_in_roi*us_to_Hz_normalisation)/(Tile_Area*4)) #Quadrant area = Tile area x 4
                CDA_Error.append(CDA_std)
                rms_Error.append(ADCmVConv*np.std(chrms.flatten()[chrms.flatten()>0]))
                DiCT_Error.append(DiCTProb[1])
        if chan == 't':
            for run in run_numbers_array:
                tilefile = spefilepath + run
                pa.LoadFile(tilefile)

                pkt     = pa.GetBranch("dstree","pk_t")   #Time of hits
                pkp     = pa.GetBranch("dstree","pk_p")   #Amplitude of each hit
                charge  = pa.GetBranch("dstree","pk_k")   #Integral of each hit
                chrms   = pa.GetBranch("dstree","ch_rms") #rms
                channelPeak   = pa.GetBranch("dstree","pk_ch")  #Channel
                channelrms   = pa.GetBranch("dstree","ch_id")  #Channel

                tilechan = int(input("Enter the channel number for tile: "))
                SNR,Amp1peMean,DN_rate_in_roi,CDA_Mean,rms,DiCTProb,SNRerr,Amp1peError,DN_rate_in_roi,CDA_std = process_channel_data(tilechan,pkp,pkt,charge,chrms,channelPeak,channelrms)
                
                BiasData.append(Bias)
                SNRData.append(SNR)
                ampData.append(Amp1peMean*ADCmVConv)
                DNData.append((DN_rate_in_roi*us_to_Hz_normalisation)/Tile_Area)
                CDAData.append(CDA_Mean)
                rmsData.append(rms*ADCmVConv)
                DiCTData.append(DiCTProb[0])

                #### Error Stuff ### 
                SNR_Error.append(SNRerr)
                amp_Error.append(Amp1peError*ADCmVConv)
                DN_Error.append((DN_rate_in_roi*us_to_Hz_normalisation)/Tile_Area)
                CDA_Error.append(CDA_std)
                rms_Error.append(ADCmVConv*np.std(chrms.flatten()[chrms.flatten()>0]))
                DiCT_Error.append(DiCTProb[1])


          
    else:
        pass
    
    print("Writing to CSV...")
    user_input = input("Enter vPDU QR code: ")
    timestamp = date.today().strftime("%Y%m%d")
    if args.channel == 'q':
        passportFile = '{}_{}_q.csv'.format(user_input,timestamp)
        with open(passportFile, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Quadrant','Bias_V','SNR','1peAmp_mV','DN_Hz_per_mm2','CDA','rms_mV','DiCT_prob','SNRError','1peAmpError_mV','DNError','CDAError','rmsStd_mV','DiCTError'])
            csv_writer.writerows(zip([1,2,3,4],BiasData,SNRData,ampData,DNData,CDAData,rmsData,DiCTData,SNR_Error,amp_Error,DN_Error,CDA_Error,rms_Error,DiCT_Error))
    elif args.channel == 't':
        passportFile = '{}_{}_t.csv'.format(user_input,timestamp)
        with open(passportFile, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Tile','Bias_V','SNR','1peAmp_mV','DN_Hz_per_mm2','CDA','rms_mV','DiCT_prob','SNRError','1peAmpError_mV','DNError','CDAError','rmsStd_mV','DiCTError'])
            csv_writer.writerows(zip([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15],BiasData,SNRData,ampData,DNData,CDAData,rmsData,DiCTData,SNR_Error,amp_Error,DN_Error,CDA_Error,rms_Error,DiCT_Error))
    
    
  





        
            




        
            
