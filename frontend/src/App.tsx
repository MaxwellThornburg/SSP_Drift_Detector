import { useState } from "react";
import FileUpload from "./components/FileUpload";
import RepoInput from "./components/RepoInput";
import ComplianceChart from "./components/ComplianceChart";

function App() {
  const [sspUploaded, setSspUploaded] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-700 px-6 py-4">
        <h1 className="text-2xl font-bold">SSP Drift Detector</h1>
        <p className="text-gray-400 text-sm">
          Detect compliance drift between your SSP and actual code
        </p>
      </header>

      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <section>
          <h2 className="text-xl font-semibold mb-3">1. Upload SSP</h2>
          <FileUpload onUploadComplete={() => setSspUploaded(true)} />
        </section>

        {sspUploaded && (
          <section>
            <h2 className="text-xl font-semibold mb-3">
              2. Analyze Repository
            </h2>
            <RepoInput onAnalysisComplete={setAnalysisResult} />
          </section>
        )}

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