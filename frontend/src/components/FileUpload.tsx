import { useRef, useState } from "react";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  disabled: boolean;
}

export function FileUpload({ onFileSelect, disabled }: FileUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File | undefined) => {
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onFileSelect(file);
  };

  return (
    <div
      className={`upload-box ${isDragging ? "dragging" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFile(e.dataTransfer.files[0]);
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        disabled={disabled}
        onChange={(e) => handleFile(e.target.files?.[0])}
        style={{ display: "none" }}
      />
      {preview ? (
        <img src={preview} alt="Leaf preview" className="preview" />
      ) : (
        <p className="upload-hint">Click or drag a leaf photo here</p>
      )}
    </div>
  );
}
