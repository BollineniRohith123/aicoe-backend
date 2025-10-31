import React, { useState } from 'react';
import './ProjectFolderTree.css';

const ProjectFolderTree = ({ projectName, folderStructure = {} }) => {
  const [expandedFolders, setExpandedFolders] = useState(new Set(['root']));

  const toggleFolder = (path) => {
    const newExpanded = new Set(expandedFolders);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    setExpandedFolders(newExpanded);
  };

  const renderTree = (node, path = 'root', level = 0) => {
    if (!node) return null;

    const isExpanded = expandedFolders.has(path);
    const hasChildren = node.children && Object.keys(node.children).length > 0;
    const files = node.files || [];

    return (
      <div key={path} className="tree-node" style={{ marginLeft: `${level * 20}px` }}>
        <div 
          className={`tree-item ${node.type === 'folder' ? 'tree-folder' : 'tree-file'}`}
          onClick={() => node.type === 'folder' && toggleFolder(path)}
        >
          {node.type === 'folder' && (
            <span className="folder-icon">
              {isExpanded ? '📂' : '📁'}
            </span>
          )}
          {node.type === 'file' && (
            <span className="file-icon">
              {getFileIcon(node.name)}
            </span>
          )}
          <span className="item-name">{node.name}</span>
          {node.type === 'folder' && hasChildren && (
            <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
          )}
        </div>

        {node.type === 'folder' && isExpanded && (
          <>
            {files.map((file, index) => (
              <div 
                key={`${path}-file-${index}`} 
                className="tree-item tree-file"
                style={{ marginLeft: `${(level + 1) * 20}px` }}
              >
                <span className="file-icon">{getFileIcon(file)}</span>
                <span className="item-name">{file}</span>
              </div>
            ))}
            {hasChildren && Object.entries(node.children).map(([name, child]) => 
              renderTree(child, `${path}/${name}`, level + 1)
            )}
          </>
        )}
      </div>
    );
  };

  const getFileIcon = (filename) => {
    if (!filename) return '📄';
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
      'md': '📝',
      'html': '🌐',
      'json': '📊',
      'csv': '📈',
      'pdf': '📕',
      'txt': '📄',
      'js': '📜',
      'css': '🎨',
      'png': '🖼️',
      'jpg': '🖼️',
      'jpeg': '🖼️',
      'svg': '🎭'
    };
    return icons[ext] || '📄';
  };

  // Default folder structure if none provided
  const defaultStructure = {
    name: projectName || 'Project',
    type: 'folder',
    children: {
      'MeetingNotes': {
        name: 'MeetingNotes',
        type: 'folder',
        files: ['structured_notes.json']
      },
      'UseCases': {
        name: 'UseCases',
        type: 'folder',
        files: ['use_cases.json']
      },
      'SystemArchitecture': {
        name: 'SystemArchitecture',
        type: 'folder',
        files: ['knowledge_enrichment.json']
      },
      'PRDDocuments': {
        name: 'PRDDocuments',
        type: 'folder',
        files: ['PRD_v1.md']
      },
      'HTML': {
        name: 'HTML',
        type: 'folder',
        children: {
          'Version1': {
            name: 'Version1',
            type: 'folder',
            children: {
              'Mockups': {
                name: 'Mockups',
                type: 'folder',
                files: ['mockup_v1.html']
              }
            }
          }
        }
      },
      'SyntheticData': {
        name: 'SyntheticData',
        type: 'folder',
        files: ['demo_data.json']
      },
      'ReviewerFeedback': {
        name: 'ReviewerFeedback',
        type: 'folder',
        files: ['review_cycle_v1.json']
      },
      'AuditLogs': {
        name: 'AuditLogs',
        type: 'folder',
        files: ['audit_log.json']
      }
    }
  };

  const structure = Object.keys(folderStructure).length > 0 ? folderStructure : defaultStructure;

  return (
    <div className="project-folder-tree-container">
      <h2 className="folder-tree-title">
        <span className="title-icon">🗂️</span>
        Project Folder Structure
      </h2>
      
      <div className="folder-tree">
        {renderTree(structure)}
      </div>
      
      <div className="folder-stats">
        <div className="stat-item">
          <span className="stat-icon">📁</span>
          <span className="stat-label">Folders:</span>
          <span className="stat-value">8</span>
        </div>
        <div className="stat-item">
          <span className="stat-icon">📄</span>
          <span className="stat-label">Files:</span>
          <span className="stat-value">8</span>
        </div>
      </div>
    </div>
  );
};

export default ProjectFolderTree;

