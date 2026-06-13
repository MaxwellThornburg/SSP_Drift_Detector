// frontend/src/components/RepoInput.tsx

import React, { useState } from 'react';

interface RepoInputProps {
  value: string;
  onChange: (value: string) => void;
}

const RepoInput: React.FC<RepoInputProps> = ({ value, onChange }) => {
  const [isValid, setIsValid] = useState(true);

  const validateUrl = (url: string): boolean => {
    if (!url) return true; // Empty is valid (optional)
    
    const githubPattern = /^https:\/\/github\.com\/[\w.-]+\/[\w.-]+(\/)?$/;
    const gitlabPattern = /^https:\/\/gitlab\.com\/[\w.-]+\/[\w.-]+(\/)?$/;
    const bitbucketPattern = /^https:\/\/bitbucket\.org\/[\w.-]+\/[\w.-]+(\/)?$/;
    const genericGitPattern = /^https?:\/\/[\w.-]+\/[\w.-]+\/[\w.-]+(\/)?$/;
    
    return githubPattern.test(url) || 
           gitlabPattern.test(url) || 
           bitbucketPattern.test(url) ||
           genericGitPattern.test(url);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    onChange(newValue);
    setIsValid(validateUrl(newValue));
  };

  return (
    <div className="w-full">
      <label 
        htmlFor="repo-url" 
        className="block text-sm font-medium text-gray-300 mb-2"
      >
        Repository URL
      </label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg
            className="h-5 w-5 text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
            />
          </svg>
        </div>
        <input
          type="url"
          id="repo-url"
          value={value}
          onChange={handleChange}
          placeholder="https://github.com/username/repository"
          className={`
            block w-full pl-10 pr-3 py-3
            bg-gray-800 border rounded-lg
            text-gray-200 placeholder-gray-500
            focus:outline-none focus:ring-2 focus:ring-blue-500
            transition-colors duration-200
            ${!isValid 
              ? 'border-red-500 focus:ring-red-500' 
              : 'border-gray-600 focus:border-blue-500'
            }
          `}
        />
        {value && isValid && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <svg
              className="h-5 w-5 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        )}
      </div>
      {!isValid && (
        <p className="mt-1 text-sm text-red-400">
          Please enter a valid repository URL
        </p>
      )}
      <p className="mt-1 text-xs text-gray-500">
        Supports GitHub, GitLab, Bitbucket, and other Git repositories
      </p>
    </div>
  );
};

export default RepoInput;