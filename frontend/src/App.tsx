import { useState } from "react";
import FileUpload from "./components/FileUpload";
import RepoInput from "./components/RepoInput";
import ComplianceChart from "./components/ComplianceChart";

// Mock analysis result type - adjust based on your actual API response
interface AnalysisResult {
  compliant: number;
  nonCompliant: number;
  notImplemented: number;
  compliancePercentage: number;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    if (!selectedFile || !repoUrl) return;
    
    setIsAnalyzing(true);
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('repo_url', repoUrl);
    
    try {
      // Using relative path since frontend is served by the same FastAPI backend in production
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setAnalysisResult(data);
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen text-white bg-gray-900">
      <header className="border-b border-gray-700 px-6 py-4">
        <h1 className="text-2xl font-bold">SSP Drift Detector</h1>
        <p className="text-gray-400 text-sm">
          Detect compliance drift between your SSP and actual code
        </p>
      </header>

      <main className="max-w-4xl mx-auto p-6 space-y-8">
        {/* Step 1: File Upload */}
        <section>
          <h2 className="text-xl font-semibold mb-3">1. Upload SSP</h2>
          <FileUpload 
            onFileSelect={setSelectedFile} 
            selectedFile={selectedFile}
          />
        </section>

        {/* Step 2: Repository Input */}
        <section>
          <h2 className="text-xl font-semibold mb-3">
            2. Enter Repository URL
          </h2>
          <p className="text-gray-400 text-sm mb-4">
            Enter the URL of the repository where the code you want to compare against the SSP is located.
          </p>
          <RepoInput 
            value={repoUrl} 
            onChange={setRepoUrl} 
          />
        </section>

        {/* Analyze Button */}
        <section>
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || !repoUrl || isAnalyzing}
            className={`
              w-full py-3 px-4 rounded-lg font-medium
              transition-colors duration-200
              ${!selectedFile || !repoUrl || isAnalyzing
                ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-500 text-white'
              }
            `}
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze Repository'}
          </button>
        </section>

        {/* Step 3: Results - shown after analysis completes */}
        {analysisResult && (
          <section>
            <h2 className="text-xl font-semibold mb-3">3. Results</h2>
            <ComplianceChart data={analysisResult} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;