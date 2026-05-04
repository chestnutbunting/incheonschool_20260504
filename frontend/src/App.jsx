import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Download, Building2, Server, Trees, HardHat, Zap, Flame, Layout } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './App.css';

const API_BASE = '/api';

const COLORS = ['#0f172a', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#64748b'];

function App() {
  const [items, setItems] = useState([]);
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [building, setBuilding] = useState('');
  const [page, setPage] = useState(1);
  const limit = 50;

  const categories = [
    { name: '전체', value: '' },
    { name: '건축', value: '건축 공사' },
    { name: '토목', value: '토목 공사' },
    { name: '조경', value: '조경 공사' },
    { name: '기계설비', value: '기계설비 공사' },
    { name: '전기', value: '전기 공사' },
    { name: '소방', value: '소방 공사' }
  ];

  const buildings = [
    { name: '전체', value: '' },
    { name: '본관동', value: '본관동' },
    { name: '소방훈련관', value: '소방훈련관' },
    { name: '소방종합훈련탑', value: '소방종합훈련탑' },
    { name: '관사동', value: '관사동' },
    { name: '기타시설', value: '기타시설' }
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchItems();
      fetchSummary();
    }, 300);
    return () => clearTimeout(timer);
  }, [search, category, building, page]);

  const fetchSummary = async () => {
    try {
      const res = await axios.get(`${API_BASE}/summary`, {
        params: { q: search, category, building }
      });
      setSummary(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchItems = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/items`, {
        params: { q: search, category, building, page, limit }
      });
      setItems(res.data.items);
      setTotal(res.data.total);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleExport = () => {
    const params = new URLSearchParams({ q: search, category, building });
    window.location.href = `${API_BASE}/export?${params.toString()}`;
  };

  const formatCurrency = (val) => {
    if (!val) return '-';
    return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(val);
  };

  const totalAmount = summary.reduce((acc, curr) => acc + curr.total, 0);

  return (
    <div className="app-container">
      <nav className="top-nav">
        <div className="logo-area">
          <Building2 size={24} />
          <span>인천소방학교 내역 관리 시스템</span>
        </div>
        
        <div className="nav-controls">
          <div className="search-container">
            <Search size={18} style={{ position: 'absolute', left: 14, top: 10, color: '#94a3b8' }} />
            <input 
              type="text" 
              className="search-input" 
              placeholder="품명 또는 규격 검색..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            />
          </div>
          <button className="export-btn" onClick={handleExport}>
            <Download size={18} />
            CSV 내보내기
          </button>
        </div>
      </nav>

      <main className="main-content">
        {/* Project Summary Slide */}
        <section className="overview-panel">
          <div>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>프로젝트 개요</h2>
            <p style={{ color: '#64748b', fontSize: '0.9rem', lineHeight: '1.6' }}>
              인천소방학교 이전 신축공사 (119 SQUARE)<br/>
              본 시스템은 표준분류체계 기반으로 정제된 내역 데이터를 실무용으로 관리하고 분석하기 위한 대시보드입니다.
            </p>
          </div>
          <div className="overview-info">
            <div className="info-box">
              <label>대지위치</label>
              <span>인천광역시 강화군 인화리</span>
            </div>
            <div className="info-box">
              <label>대지면적</label>
              <span>29,934㎡</span>
            </div>
            <div className="info-box">
              <label>총 사업비</label>
              <span style={{ color: '#3b82f6' }}>430억</span>
            </div>
          </div>
        </section>

        {/* Filters */}
        <section className="filter-section">
          <div className="filter-group">
            <span className="filter-label">공사 구분</span>
            <div className="tabs">
              {categories.map(cat => (
                <button 
                  key={cat.name}
                  className={`tab-btn ${category === cat.value ? 'active' : ''}`}
                  onClick={() => { setCategory(cat.value); setPage(1); }}
                >
                  {cat.name}
                </button>
              ))}
            </div>
          </div>
          <div className="filter-group">
            <span className="filter-label">건물 동</span>
            <div className="tabs">
              {buildings.map(b => (
                <button 
                  key={b.name}
                  className={`tab-btn ${building === b.value ? 'active' : ''}`}
                  onClick={() => { setBuilding(b.value); setPage(1); }}
                >
                  {b.name}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Cards */}
        <section className="stats-grid">
          <div className="stat-card">
            <span className="label">검색 결과 합계</span>
            <span className="value" style={{ color: '#3b82f6' }}>{formatCurrency(totalAmount)}</span>
          </div>
          <div className="stat-card">
            <span className="label">데이터 건수</span>
            <span className="value">{total.toLocaleString()}건</span>
          </div>
          <div className="stat-card">
            <span className="label">현재 페이지</span>
            <span className="value">{page} / {Math.ceil(total / limit) || 1}</span>
          </div>
        </section>

        {/* Charts */}
        <section className="charts-grid">
          <div className="chart-card">
            <h3>공사별 예산 분포</h3>
            <div style={{ flex: 1 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={summary} layout="vertical" margin={{ left: 30, right: 30 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
                  <XAxis type="number" hide />
                  <YAxis dataKey="category" type="category" width={100} fontSize={12} tickFormatter={v => v.replace(' 공사', '')} />
                  <Tooltip formatter={val => formatCurrency(val)} />
                  <Bar dataKey="total" fill="#0f172a" radius={[0, 4, 4, 0]} barSize={24}>
                    {summary.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="chart-card">
            <h3>예산 점유율 (%)</h3>
            <div style={{ flex: 1 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={summary}
                    innerRadius="50%"
                    outerRadius="80%"
                    paddingAngle={4}
                    dataKey="total"
                    nameKey="category"
                    label={({ name, percent }) => `${name.replace(' 공사', '')} ${(percent * 100).toFixed(1)}%`}
                  >
                    {summary.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip formatter={val => formatCurrency(val)} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* Table */}
        <section className="table-container">
          <div className="table-wrapper">
            {loading ? (
              <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>데이터를 불러오는 중입니다...</div>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>동</th>
                    <th>공사구분</th>
                    <th>대공종</th>
                    <th>품명</th>
                    <th>규격</th>
                    <th style={{ textAlign: 'right' }}>수량</th>
                    <th>단위</th>
                    <th style={{ textAlign: 'right' }}>합계금액</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map(item => (
                    <tr key={item.id}>
                      <td style={{ color: '#64748b' }}>{item.WHERE2_동}</td>
                      <td><span className="badge" style={{ background: '#f1f5f9' }}>{item.HOW1_공사}</span></td>
                      <td>{item.HOW2_대공종}</td>
                      <td style={{ fontWeight: 600 }}>{item.HOW4_품명}</td>
                      <td style={{ color: '#64748b' }}>{item.HOW5_규격}</td>
                      <td style={{ textAlign: 'right' }}>{item.R2_수량?.toLocaleString()}</td>
                      <td>{item.R1_단위}</td>
                      <td style={{ textAlign: 'right', fontWeight: 700 }}>{formatCurrency(item.R10_합계_금액)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div className="pagination">
            <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
              전체 <strong>{total.toLocaleString()}</strong>건 중 {items.length}건 표시
            </div>
            <div className="pagination-controls">
              <button className="page-btn" disabled={page === 1} onClick={() => setPage(p => p - 1)}>이전</button>
              <button className="page-btn" disabled={page >= Math.ceil(total / limit)} onClick={() => setPage(p => p + 1)}>다음</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
