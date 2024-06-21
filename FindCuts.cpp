// Background studies and sensitivity - 1 scan point in sqrt(s)
#include <TH1.h>
#include <TH2.h>
#include <TStyle.h> 
#include <TString.h> 
#include <TObject.h>
#include <TCanvas.h> 
#include <TGraph.h> 
#include <TMultiGraph.h> 
#include <TAxis.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <stdexcept>
#include <TMath.h>
#include <TTree.h>
#include <TVector3.h>
#include <regex>

using namespace std;

void FindCuts(){

    ifstream TxtIn("Elist.txt");

    double pi2 = TMath::Pi()*2;
    double MassEl = 0.511; //in MeV
    TVector3 TargetPosition (0.,0.,-1028.); //read by MC full
    TVector3 ECalPosition (0.,0.,2672.); //read by MC full
    double RECal = 304.5; //external radius of ECal 
    double RMax = 270.;  // in mm

    //creating output file with Rmin, Rmax, Emin, Emax
    ofstream FileOut("info.csv");

    //CUTS TOMMASO - they are defined here once for type of process
    double SqrtS, BeamMomentum;
    double BG, Beta, Gamma;
    TVector3 BoostMom;
    double RMin, Energy_max, Energy_min;
    double thetaMax, thetaMin;
    double EMin, EMax;

    double EBeam, PoT;
    int i = 0;
    FileOut << "id" << "," << "ecms" << "," << "ebeam" << "," << "tmin" << "," << "tmax" << "," << "emin" << "," << "emax" << "\n";

    while (TxtIn >> EBeam){
        SqrtS = TMath::Sqrt(2.*MassEl*EBeam); // in MeV
        BeamMomentum = TMath::Sqrt(EBeam*EBeam - MassEl*MassEl); //in MeV
        BG = BeamMomentum/SqrtS; // mBeta mGamma
        Gamma = TMath::Sqrt(BG*BG + 1.);
        Beta = BG/Gamma;
        BoostMom.SetXYZ(0, 0, ECalPosition.Z()-TargetPosition.Z());
        BoostMom *= (Beta/BoostMom.Mag());

        double tanQMax = RMax/(ECalPosition.Z()-TargetPosition.Z());
        double tMax = 2*TMath::ATan(Gamma*tanQMax);

        // cout << EBeam << " " << tMax << endl;
        RMin = (ECalPosition.Z()-TargetPosition.Z())*TMath::Tan(0.5*TMath::Pi()-0.5*tMax)/Gamma;

        double tanQMin = RMin/(ECalPosition.Z()-TargetPosition.Z());
        double tMin = 2*TMath::ATan(Gamma*tanQMin);

        thetaMax = tMax*180/TMath::Pi();
        thetaMin = tMin*180/TMath::Pi();
       
        Energy_max = SqrtS*Gamma*0.5*(1.-TMath::Cos(tMax)); 
        Energy_min = SqrtS*Gamma*0.5*(1.+TMath::Cos(tMax)); 

        EMax = Gamma*(Energy_max - Beta*sqrt(Energy_max*Energy_max - MassEl*MassEl)*TMath::Cos(TMath::ATan(tanQMax)));
        EMin = Gamma*(Energy_min - Beta*sqrt(Energy_min*Energy_min - MassEl*MassEl)*TMath::Cos(TMath::ATan(tanQMin)));

        cout << "GeneralInfo: run-level info for run from DYNAMIC CUTS at " << EBeam <<" MeV" << " Pbeam = " << BeamMomentum << endl;
        cout << " target = { " << TargetPosition.X()<< " , "<< TargetPosition.Y() << " , " << TargetPosition.Z() << 
                " }; COG = { " << ECalPosition.X() << " , " << ECalPosition.Y() << " , "<< ECalPosition.Z() << " }" << endl; 
        cout << " sqrt(s) = " << SqrtS << " BG = " << BG << " Beta = " << Beta << endl;
        cout << " energyRange = { " << Energy_min << " , " << Energy_max << " }; radiusRange = { " << RMin << " , " << RMax << " }" << endl;
        cout << " AngularRange CoM = { " << thetaMin << " , " << thetaMax << " }" << endl;
        
        FileOut << i << "," << SqrtS*1e-3 << "," << EBeam*1e-3 << "," << thetaMin << "," << thetaMax << "," << EMin*1e-3 << "," << EMax*1e-3 << "\n";
        i++;
    }

    TxtIn.close();
    FileOut.close();
}
