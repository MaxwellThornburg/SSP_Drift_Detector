import { useState } from "react";
import FileUpload from "./components/FileUpload";
import RepoInput from "./components/RepoInput";
import ComplianceChart from "./components/ComplianceChart";

function App() {
  const [sspData, setSspData] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 relative">
      {/* Brushed metal texture overlay */}
      <div className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`
        }}
      />
      
      {/* DoD Seal */}
      <div className="mb-6 relative z-10">
        <img 
          src="/dod-seal.png" 
          alt="Department of Defense" 
          className="dod-seal"
        />
      </div>

      {/* Title */}
      <h1 className="text-3xl font-bold tracking-widest text-gray-200 mb-2 uppercase relative z-10">
        SSP Drift Detector
      </h1>
      <p className="text-gray-500 text-sm mb-12 tracking-wider relative z-10">
        COMPLIANCE MONITORING SYSTEM
      </p>

      {/* Main Content */}
      <div className="w-full max-w-4xl relative z-10">
        {!sspData ? (
          <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
            <FileUpload onUploadComplete={setSspData} />
          </div>
        ) : !analysisResult ? (
          <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
            <RepoInput 
              sspData={sspData}
              onAnalysisComplete={setAnalysisResult} 
            />
          </div>
        ) : (
          <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
            <ComplianceChart data={analysisResult} />
          </div>
        )}
      </div>

      {/* Window controls (since frameless) */}
      <div className="absolute top-4 right-4 flex gap-2 z-20">
        <button 
          onClick={() => window.pywebview.api.close()}
          className="w-3 h-3 rounded-full bg-red-500 hover:bg-red-400 transition-colors"
        />
      </div>
    </div>
  );
}

export default App;